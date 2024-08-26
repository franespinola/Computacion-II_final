import socket
import threading
from carta import carta
from restaurante import Restaurante
from collections import defaultdict
from colorama import Fore, Style
import logging
import select

# Configuración del logging
logging.basicConfig(filename='servidor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def imprimir_mensaje(mensaje, tipo='INFO'):
    """Imprime un mensaje formateado en la terminal."""
    if tipo == 'INFO':
        print(f"{Fore.BLUE}[INFO] {Style.RESET_ALL}{mensaje}")
    elif tipo == 'ERROR':
        print(f"{Fore.RED}[ERROR] {Style.RESET_ALL}{mensaje}")
    elif tipo == 'SUCCESS':
        print(f"{Fore.GREEN}[SUCCESS] {Style.RESET_ALL}{mensaje}")
    else:
        print(f"{mensaje}")


# Diccionario para almacenar los sockets de los clientes y sus pedidos por ID de pedido
clientes_pedidos = {}
clientes_sockets = {}

def handle_client(client_socket):
    """Maneja la conexión con un cliente."""
    restaurante = Restaurante(carta)
    direccion_cliente = client_socket.getpeername()
    direccion_cliente_formateada = f"{direccion_cliente[0]}:{direccion_cliente[1]}"
    clientes_sockets[direccion_cliente_formateada] = (client_socket, restaurante)
    imprimir_mensaje(f"Conexión establecida con el cliente {direccion_cliente_formateada}", 'SUCCESS')
    logging.info(f"Conexión establecida con el cliente {direccion_cliente_formateada}")

    while True:
        opcion = client_socket.recv(1024).decode().strip()

        # Verificar si el mensaje recibido está vacío
        if not opcion:
            imprimir_mensaje(f"Conexión cerrada por el cliente {direccion_cliente_formateada}", 'INFO')
            logging.info(f"Conexión cerrada por el cliente {direccion_cliente_formateada}")
            break

        imprimir_mensaje(f"Opción recibida: {opcion}, Cliente: {direccion_cliente_formateada}", 'INFO')

        # --- Mostrar carta ---
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
            enviar_pedido_a_cocina_y_salir(client_socket, restaurante)

    # Cerrar la conexión y eliminar el cliente del diccionario al salir del bucle
    client_socket.close()
    del clientes_sockets[direccion_cliente_formateada]
    imprimir_mensaje(f"Conexión cerrada y recursos liberados para el cliente {direccion_cliente_formateada}", 'INFO')
    logging.info(f"Conexión cerrada y recursos liberados para el cliente {direccion_cliente_formateada}")


def mostrar_carta(client_socket):
    """Envía la carta al cliente."""
    productos_por_categoria = defaultdict(list)
    respuesta = ""
    for producto in carta:
        productos_por_categoria[producto.categoria].append(producto)
    for categoria in productos_por_categoria:
        respuesta += f"\n\n{Fore.GREEN}{categoria}{Style.RESET_ALL}:\n\n"
        respuesta += "\n".join(str(producto) for producto in productos_por_categoria[categoria])
    client_socket.sendall(respuesta.encode())
    logging.info(f"Cliente {client_socket.getpeername()} - Carta mostrada.")

def tomar_pedido(client_socket, restaurante):
    """Toma un pedido del cliente."""
    respuesta = f"{Fore.GREEN}Tomando pedido...{Style.RESET_ALL}"
    client_socket.sendall(respuesta.encode())
    nombre = client_socket.recv(1024).decode()
    producto_id = int(client_socket.recv(1024).decode())
    cantidad = int(client_socket.recv(1024).decode())
    observaciones = client_socket.recv(1024).decode()
    producto = next((prod for prod in carta if prod.id == producto_id), None)
    if producto is not None:
        restaurante.tomar_pedido(nombre, producto, cantidad, observaciones)
        # Obtener el ID del pedido recién creado
        id_pedido = restaurante.pedidos[-1].id
        clientes_pedidos[id_pedido] = client_socket
        client_socket.sendall("Pedido tomado con éxito.".encode())
        logging.info(f"Cliente {client_socket.getpeername()} - Pedido tomado: {restaurante.pedidos[-1]}")
    else:
        logging.error(f"Cliente {client_socket.getpeername()} - Error: Producto no encontrado en la carta.")
        client_socket.sendall("Error: Producto no encontrado en la carta.".encode())

def mostrar_pedido(client_socket, restaurante):
    """Muestra los pedidos del cliente."""
    pedidos = restaurante.mostrar_pedidos()
    client_socket.sendall(pedidos.encode())
    if pedidos == "No hay pedidos.":
        logging.info(f"Cliente {client_socket.getpeername()} - No hay pedidos.")
        return
    else:
        logging.info(f"Cliente {client_socket.getpeername()} - Pedidos mostrados")
    pregunta = client_socket.recv(1024).decode()
    if pregunta.lower() == 's':
        nombre = client_socket.recv(1024).decode()
        producto_id = int(client_socket.recv(1024).decode())
        cantidad = int(client_socket.recv(1024).decode())
        observaciones = client_socket.recv(1024).decode()
        producto = next((prod for prod in carta if prod.id == producto_id), None)
        if producto is not None:
            restaurante.tomar_pedido(nombre, producto, cantidad, observaciones)
            client_socket.sendall(restaurante.mostrar_pedidos().encode())
        else:
            logging.error(f"Cliente {client_socket.getpeername()} - Error: Producto no encontrado en la carta.")
            client_socket.sendall("Error: Producto no encontrado en la carta.".encode())


def modificar_pedido(client_socket, restaurante):
    """Modifica un pedido del cliente."""
    if restaurante.mostrar_pedidos() == "No hay pedidos.":
        client_socket.sendall("No hay pedidos.".encode())
        return
    mensaje = f"{Fore.YELLOW}Modificando pedido...{Style.RESET_ALL}"
    client_socket.sendall(mensaje.encode())
    id_pedido = int(client_socket.recv(1024).decode())
    if not restaurante.pedido_existe(id_pedido):
        client_socket.sendall("El pedido con el ID proporcionado no existe.".encode())
        logging.error(f"Cliente {client_socket.getpeername()} - Error: Pedido no encontrado para su modificación.")
    else:
        logging.info(f"Cliente {client_socket.getpeername()} - Pedido modificado: {id_pedido}")
        client_socket.sendall("Pedido modificado con éxito.".encode())
        producto_id = int(client_socket.recv(1024).decode())
        cantidad = int(client_socket.recv(1024).decode())
        observaciones = client_socket.recv(1024).decode()
        producto = next((prod for prod in carta if prod.id == producto_id), None)
        if producto is not None:
            client_socket.sendall(restaurante.modificar_pedido(id_pedido, producto, cantidad, observaciones).encode())
        else:
            logging.error(f"Cliente {client_socket.getpeername()} - Error: Producto no encontrado en la carta.")
            client_socket.sendall("Error: Producto no encontrado en la carta.".encode())

def eliminar_pedido(client_socket, restaurante):
    """Elimina un pedido del cliente."""
    if restaurante.mostrar_pedidos() == "No hay pedidos.":
        client_socket.sendall("No hay pedidos.".encode())
        return
    mensaje = f"{Fore.RED}Eliminando pedido.....{Style.RESET_ALL}"
    client_socket.sendall(mensaje.encode())
    id_pedido = client_socket.recv(1024).decode()
    if not restaurante.pedido_existe(id_pedido):
        logging.error(f"Cliente {client_socket.getpeername()} - Error: Pedido no encontrado para su eliminación.")
        client_socket.sendall("El pedido con el ID proporcionado no existe.".encode())
    else:
        logging.info(f"Cliente {client_socket.getpeername()} - Pedido eliminado: {id_pedido}")
        restaurante.eliminar_pedido(id_pedido)
        client_socket.sendall("Pedido eliminado con éxito.".encode())
        print(f"Cliente {client_socket.getpeername()} - Pedido eliminado: {id_pedido}")

def enviar_pedido_a_cocina_y_salir(client_socket, restaurante):
    """Envía el pedido a la cocina y reinicia los pedidos del cliente."""
    client_socket.sendall(restaurante.mostrar_pedidos().encode())
    if restaurante.mostrar_pedidos() == "No hay pedidos.":
        return
    pregunta = client_socket.recv(1024).decode()
    if pregunta.lower() == 's':
        logging.info(f"Cliente {client_socket.getpeername()} - Pedido enviado a cocina")
        direccion_cliente = f"{client_socket.getpeername()[0]}:{client_socket.getpeername()[1]}"
        enviar_pedido_a_cocina(restaurante.mostrar_pedidos(), direccion_cliente)
        client_socket.sendall("Pedido enviado a cocina. Espere a ser llamado.".encode())
        print(f"Cliente {client_socket.getpeername()} - Pedido enviado a cocina: {restaurante.mostrar_pedidos()}")

def escuchar_confirmaciones_cocina():
    """Escucha las confirmaciones de la cocina en un hilo separado."""
    cocina_host = 'localhost'
    cocina_port = 50009  # Puerto para la comunicación con la cocina
    cocina_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cocina_socket.bind((cocina_host, cocina_port))
    cocina_socket.listen(5)

    while True:
        conn, addr = cocina_socket.accept()
        confirmacion = conn.recv(1024).decode()
        print(f"Confirmación recibida de la cocina: {confirmacion}")

        # Extraer la dirección del cliente desde el final de la confirmación
        try:
            # Separamos la dirección IP del cliente usando la coma
            direccion_cliente = confirmacion.split(",")[-1].strip()
            print(f"Dirección del cliente extraída: {direccion_cliente}")

            # Buscamos el socket del cliente usando la dirección IP y puerto
            if direccion_cliente in clientes_sockets:
                cliente_socket, _ = clientes_sockets[direccion_cliente]
                cliente_socket.sendall("Pedido listo para retirar".encode())
                print(f"Notificación enviada al cliente {direccion_cliente}")
            else:
                print(f"No se encontró cliente para la dirección {direccion_cliente}")
        except Exception as e:
            print(f"Error al procesar la confirmación de la cocina: {e}")

        conn.close()


def enviar_pedido_a_cocina(pedido, direccion_cliente):
    """Envía el pedido a la cocina."""
    cocina_host = 'localhost'
    cocina_port = 50008  # Puerto donde está escuchando la cocina
    cocina_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cocina_socket.connect((cocina_host, cocina_port))
    cocina_socket.sendall(f"{pedido},{direccion_cliente}".encode())
    cocina_socket.close()

def server():
    """Inicia el servidor."""
    PORT = 50007
    server_sockets = []

    # Direcciones específicas para escuchar
    direcciones = [
        ('192.168.1.42', PORT, socket.AF_INET),
        ('fda8:4ac5:c10a:1a8f:f299:931d:e6be:9dd5', PORT, socket.AF_INET6)
    ]

    # Intentar crear y vincular sockets para las direcciones específicas
    for direccion, puerto, familia in direcciones:
        try:
            server_socket = socket.socket(familia, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            imprimir_mensaje(f"Servidor escuchando en {direccion}:{puerto}", 'SUCCESS')
            server_socket.bind((direccion, puerto))
            server_socket.listen(5)
            server_sockets.append(server_socket)
        except OSError as e:
            imprimir_mensaje(f"Error al crear o vincular socket en {direccion}:{puerto} - {e}", 'ERROR')
            logging.error(f"Error al crear o vincular socket en {direccion}:{puerto} - {e}")

    if not server_sockets:
        imprimir_mensaje("No se pudo crear ningún socket para las direcciones especificadas", 'ERROR')
        return

    # Iniciar el hilo para escuchar las confirmaciones de la cocina
    threading.Thread(target=escuchar_confirmaciones_cocina, daemon=True).start()

    while True:
        readable, _, _ = select.select(server_sockets, [], [])
        for s in readable:
            conn, addr = s.accept()
            direccion_cliente_formateada = f"{addr[0]}:{addr[1]}"
            imprimir_mensaje(f"Conexión aceptada desde {direccion_cliente_formateada}", 'SUCCESS')
            client_thread = threading.Thread(target=handle_client, args=(conn,))
            client_thread.start()
server()
