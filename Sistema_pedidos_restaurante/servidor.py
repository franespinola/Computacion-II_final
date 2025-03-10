import socket
import threading
import logging
from collections import defaultdict
from colorama import Fore, Style
from carta import carta
from restaurante import Restaurante
import queue
import configparser

# Configurar logging
logging.basicConfig(filename='servidor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def imprimir_mensaje(mensaje, tipo='INFO'):
    if tipo == 'INFO':
        print(f"{Fore.BLUE}[INFO] {Style.RESET_ALL}{mensaje}")
    elif tipo == 'ERROR':
        print(f"{Fore.RED}[ERROR] {Style.RESET_ALL}{mensaje}")
    elif tipo == 'SUCCESS':
        print(f"{Fore.GREEN}[SUCCESS] {Style.RESET_ALL}{mensaje}")
    else:
        print(mensaje)

# Diccionario para almacenar sockets y restaurantes por cliente
clientes_sockets = {}

# Cola de pedidos compartida con la cocina
pedidos_queue = queue.Queue()

def handle_client(client_socket):
    """
    Función principal que maneja la comunicación con un cliente.
    Se ejecuta en un hilo independiente para cada cliente.
    """
    direccion_cliente = None
    cliente_id = None
    restaurante = None
    pedido_enviado = False  # Bandera para verificar si se envió un pedido
    desconexion_inesperada = False  # Bandera de desconexión

    try:
        # Crear instancia de restaurante para este cliente
        restaurante = Restaurante(carta)

        direccion_cliente = client_socket.getpeername()  # (ip, puerto)
        cliente_id = f"{direccion_cliente[0]}:{direccion_cliente[1]}"

        # Guardamos el socket y el restaurante para este cliente
        clientes_sockets[cliente_id] = (client_socket, restaurante)

        imprimir_mensaje(f"Conexión establecida con {cliente_id}", 'SUCCESS')
        logging.info(f"Conexión establecida con {cliente_id}")

        while True:
            try:
                opcion = client_socket.recv(1024).decode().strip()
                if not opcion:
                    # Si no hay datos, el cliente cerró la conexión
                    imprimir_mensaje(f"Conexión cerrada por {cliente_id}", 'INFO')
                    logging.info(f"Conexión cerrada por {cliente_id}")
                    break

                imprimir_mensaje(f"Opción {opcion} recibida de {cliente_id}", 'INFO')

                if opcion == "1":
                    mostrar_carta(client_socket)
                elif opcion == "2":
                    tomar_pedido(client_socket, restaurante)
                elif opcion == "3":
                    mostrar_pedido(client_socket, restaurante)
                elif opcion == "4":
                    modificar_pedido(client_socket, restaurante)
                elif opcion == "5":
                    eliminar_pedido(client_socket, restaurante)
                elif opcion == "6":
                    # Devuelve True si se envió un pedido a la cola
                    pedido_enviado = enviar_pedido_a_cocina_y_salir(client_socket, restaurante)
            except ConnectionResetError:
                desconexion_inesperada = True
                imprimir_mensaje(f"Cliente {cliente_id} cerró la ventana inesperadamente.", 'ERROR')
                break
            except BrokenPipeError:
                desconexion_inesperada = True
                imprimir_mensaje(f"No se puede enviar/recibir datos. Conexión rota con {cliente_id}.", 'ERROR')
                break
            except OSError as e:
                desconexion_inesperada = True
                imprimir_mensaje(f"Error de conexión con {cliente_id}: {e}", 'ERROR')
                break
            except Exception as e:
                # Captura cualquier otro error inesperado
                desconexion_inesperada = True
                imprimir_mensaje(f"Error inesperado en el loop con {cliente_id}: {e}", 'ERROR')
                break

    except Exception as e:
        imprimir_mensaje(f"Error general con {cliente_id if cliente_id else ''}: {e}", 'ERROR')

    finally:
        client_socket.close()
        if cliente_id in clientes_sockets:
            del clientes_sockets[cliente_id]
        
        if desconexion_inesperada:
            imprimir_mensaje(f"Conexión cerrada inesperadamente para {cliente_id}", 'ERROR')
        else:
            if pedido_enviado:
                imprimir_mensaje(f"Pedido listo y conexión cerrada para {cliente_id}", 'INFO')
                logging.info(f"Pedido listo y conexión cerrada para {cliente_id}")
            else:
                imprimir_mensaje(f"Conexión cerrada con {cliente_id} sin pedido.", 'INFO')

def mostrar_carta(client_socket):
    """
    Envía la carta al cliente, agrupada por categorías.
    """
    try:
        productos_por_categoria = defaultdict(list)
        for producto in carta:
            productos_por_categoria[producto.categoria].append(producto)

        respuesta = ""
        for categoria, productos in productos_por_categoria.items():
            respuesta += f"\n\n{Fore.GREEN}{categoria}{Style.RESET_ALL}:\n"
            for p in productos:
                respuesta += f"{p}\n"

        client_socket.sendall(respuesta.encode())
    except (ConnectionResetError, BrokenPipeError):
        imprimir_mensaje("Error: El cliente cerró la conexión al enviar la carta.", 'ERROR')
    except OSError as e:
        imprimir_mensaje(f"Error de envío de carta: {e}", 'ERROR')
    except Exception as e:
        imprimir_mensaje(f"Error inesperado en mostrar_carta: {e}", 'ERROR')

def tomar_pedido(client_socket, restaurante):
    """
    Recibe datos para tomar un nuevo pedido: nombre, ID de producto, cantidad, observaciones.
    Valida y almacena el pedido en el restaurante asociado a este cliente.
    """
    try:
        # Avisamos que estamos tomando pedido
        client_socket.sendall("Tomando pedido...".encode())

        nombre = client_socket.recv(1024).decode()
        producto_id = int(client_socket.recv(1024).decode())
        cantidad = int(client_socket.recv(1024).decode())
        observaciones = client_socket.recv(1024).decode()

        producto = next((p for p in carta if p.id == producto_id), None)
        if producto:
            restaurante.tomar_pedido(nombre, producto, cantidad, observaciones)
            client_socket.sendall("Pedido tomado con éxito.".encode())
        else:
            client_socket.sendall("Error: Producto no encontrado en la carta.".encode())

    except (ValueError, ConnectionResetError, BrokenPipeError) as e:
        imprimir_mensaje(f"Error al tomar pedido: {e}", 'ERROR')
    except OSError as e:
        imprimir_mensaje(f"Error de envío/recepción al tomar pedido: {e}", 'ERROR')
    except Exception as e:
        imprimir_mensaje(f"Error inesperado en tomar_pedido: {e}", 'ERROR')

def mostrar_pedido(client_socket, restaurante):
    """
    Muestra todos los pedidos y pregunta si desea agregar otro producto.
    """
    try:
        pedidos = restaurante.mostrar_pedidos()
        client_socket.sendall(pedidos.encode())

        if pedidos == "No hay pedidos.":
            return

        pregunta = client_socket.recv(1024).decode().lower()
        if pregunta == 's':
            nombre = client_socket.recv(1024).decode()
            producto_id = int(client_socket.recv(1024).decode())
            cantidad = int(client_socket.recv(1024).decode())
            observaciones = client_socket.recv(1024).decode()

            producto = next((p for p in carta if p.id == producto_id), None)
            if producto:
                restaurante.tomar_pedido(nombre, producto, cantidad, observaciones)
                # Enviamos la lista de pedidos actualizada
                client_socket.sendall(restaurante.mostrar_pedidos().encode())
            else:
                client_socket.sendall("Error: Producto no encontrado en la carta.".encode())

    except (ValueError, ConnectionResetError, BrokenPipeError) as e:
        imprimir_mensaje(f"Error al mostrar/actualizar pedido: {e}", 'ERROR')
    except OSError as e:
        imprimir_mensaje(f"Error de envío/recepción al mostrar pedido: {e}", 'ERROR')
    except Exception as e:
        imprimir_mensaje(f"Error inesperado en mostrar_pedido: {e}", 'ERROR')

def modificar_pedido(client_socket, restaurante):
    """
    Permite modificar un pedido existente: se pide el ID, y luego se actualiza 
    con un nuevo producto, cantidad y observaciones.
    """
    try:
        # Verificamos si hay pedidos
        if restaurante.mostrar_pedidos() == "No hay pedidos.":
            client_socket.sendall("No hay pedidos.".encode())
            return

        client_socket.sendall("Modificando pedido...".encode())

        id_pedido = int(client_socket.recv(1024).decode())
        if not restaurante.pedido_existe(id_pedido):
            client_socket.sendall("El pedido con el ID proporcionado no existe.".encode())
        else:
            # Avisamos que el pedido existe y procedemos a modificar
            client_socket.sendall("Pedido modificado con éxito.".encode())

            producto_id = int(client_socket.recv(1024).decode())
            cantidad = int(client_socket.recv(1024).decode())
            observaciones = client_socket.recv(1024).decode()

            producto = next((p for p in carta if p.id == producto_id), None)
            if producto:
                result = restaurante.modificar_pedido(id_pedido, producto, cantidad, observaciones)
                client_socket.sendall(result.encode())
            else:
                client_socket.sendall("Error: Producto no encontrado en la carta.".encode())

    except (ValueError, ConnectionResetError, BrokenPipeError) as e:
        imprimir_mensaje(f"Error al modificar pedido: {e}", 'ERROR')
    except OSError as e:
        imprimir_mensaje(f"Error de envío/recepción al modificar pedido: {e}", 'ERROR')
    except Exception as e:
        imprimir_mensaje(f"Error inesperado en modificar_pedido: {e}", 'ERROR')

def eliminar_pedido(client_socket, restaurante):
    """
    Elimina un pedido por su ID.
    """
    try:
        if restaurante.mostrar_pedidos() == "No hay pedidos.":
            client_socket.sendall("No hay pedidos.".encode())
            return

        client_socket.sendall("Eliminando pedido...".encode())

        id_pedido = client_socket.recv(1024).decode()
        if not restaurante.pedido_existe(id_pedido):
            client_socket.sendall("El pedido con el ID proporcionado no existe.".encode())
        else:
            restaurante.eliminar_pedido(id_pedido)
            client_socket.sendall("Pedido eliminado con éxito.".encode())

    except (ConnectionResetError, BrokenPipeError) as e:
        imprimir_mensaje(f"Error al eliminar pedido: {e}", 'ERROR')
    except OSError as e:
        imprimir_mensaje(f"Error de envío/recepción al eliminar pedido: {e}", 'ERROR')
    except Exception as e:
        imprimir_mensaje(f"Error inesperado en eliminar_pedido: {e}", 'ERROR')

def enviar_pedido_a_cocina_y_salir(client_socket, restaurante):
    """
    Envía los pedidos del cliente a la cola de la cocina y limpia la lista de pedidos.
    Devuelve True si se envió el pedido, False en caso contrario.
    """
    try:
        pedidos = restaurante.mostrar_pedidos()
        client_socket.sendall(pedidos.encode())
        
        if pedidos == "No hay pedidos.":
            return False

        pregunta = client_socket.recv(1024).decode().lower()
        if pregunta == 's':
            direccion_cliente = f"{client_socket.getpeername()[0]}:{client_socket.getpeername()[1]}"
            pedidos_queue.put(f"{restaurante.mostrar_pedidos()},{direccion_cliente}")
            client_socket.sendall("Pedido enviado a cocina. Espere a ser llamado.".encode())

            # Limpiamos los pedidos del cliente en el restaurante
            restaurante.pedidos.clear()
            return True
    except (ConnectionResetError, BrokenPipeError) as e:
        imprimir_mensaje(f"Error al enviar pedido a cocina: {e}", 'ERROR')
    except OSError as e:
        imprimir_mensaje(f"Error de envío/recepción al enviar pedido a cocina: {e}", 'ERROR')
    except Exception as e:
        imprimir_mensaje(f"Error inesperado en enviar_pedido_a_cocina_y_salir: {e}", 'ERROR')

    return False

def aceptar_conexiones(server_socket):
    """
    Acepta conexiones entrantes en un bucle infinito y lanza un hilo para cada cliente.
    """
    while True:
        try:
            conn, addr = server_socket.accept()
            imprimir_mensaje(f"Conexión aceptada desde {addr}", 'SUCCESS')
            hilo_cliente = threading.Thread(target=handle_client, args=(conn,), daemon=True)
            hilo_cliente.start()
        except OSError as e:
            imprimir_mensaje(f"Error al aceptar conexiones: {e}", 'ERROR')
            break
        except Exception as e:
            imprimir_mensaje(f"Error inesperado en aceptar_conexiones: {e}", 'ERROR')
            break

def server():
    """
    Configura el servidor usando los parámetros de 'configServidor.ini' y 
    crea sockets para IPv4/IPv6 (según disponibilidad), luego inicia hilos
    para aceptar conexiones en cada uno de ellos.
    """
    try:
        config = configparser.ConfigParser()
        config.read('configServidor.ini')

        if 'SERVER' not in config or 'port' not in config['SERVER']:
            print(f"{Fore.RED}Falta la configuración en configServidor.ini (sección SERVER: port).{Style.RESET_ALL}")
            exit(1)

        PORT = int(config['SERVER']['port'])
        server_sockets = []

        # Usamos AF_UNSPEC para obtener información IPv4/IPv6.
        direcciones = socket.getaddrinfo(None, PORT, socket.AF_UNSPEC,
                                         socket.SOCK_STREAM, 0, socket.AI_PASSIVE)

        for familia, tipo, proto, _, sockaddr in direcciones:
            try:
                s = socket.socket(familia, tipo, proto)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(sockaddr)
                s.listen(5)
                imprimir_mensaje(f"Servidor escuchando en {sockaddr}", 'SUCCESS')
                server_sockets.append(s)
            except OSError as e:
                imprimir_mensaje(f"Error al crear socket en {sockaddr}: {e}", 'ERROR')

        # Iniciamos un hilo por cada socket que haya sido exitoso
        for sock in server_sockets:
            hilo = threading.Thread(target=aceptar_conexiones, args=(sock,), daemon=True)
            hilo.start()

    except KeyboardInterrupt:
        imprimir_mensaje("\nServidor detenido por el usuario.", 'ERROR')
    except Exception as e:
        imprimir_mensaje(f"Error inesperado al iniciar el servidor: {e}", 'ERROR')
