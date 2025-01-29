import socket
import threading
import queue
import time
from carta import carta
from restaurante import Restaurante
from collections import defaultdict
from colorama import Fore, Style
import logging

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

# Diccionario para almacenar los sockets de los clientes
clientes_sockets = {}

# Cola de pedidos para la cocina (internamente)
pedidos_queue = queue.Queue()

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

        # Verificar si el mensaje recibido está vacío (cliente desconectado)
        if not opcion:
            imprimir_mensaje(f"Conexión cerrada por el cliente {direccion_cliente_formateada}", 'INFO')
            logging.info(f"Conexión cerrada por el cliente {direccion_cliente_formateada}")
            break

        imprimir_mensaje(f"Opción recibida: {opcion}, Cliente: {direccion_cliente_formateada}", 'INFO')

        # --- Opciones del cliente ---
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

    # Cerrar la conexión al salir del bucle
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
    """Envía el pedido a la cocina (a la cola interna) y reinicia los pedidos del cliente."""
    pedidos = restaurante.mostrar_pedidos()
    client_socket.sendall(pedidos.encode())
    if pedidos == "No hay pedidos.":
        return
    pregunta = client_socket.recv(1024).decode()
    if pregunta.lower() == 's':
        logging.info(f"Cliente {client_socket.getpeername()} - Pedido enviado a cocina")
        direccion_cliente = f"{client_socket.getpeername()[0]}:{client_socket.getpeername()[1]}"
        # Formato del pedido en la cola: "descripcion_de_pedidos,direccion_cliente"
        pedidos_queue.put(f"{restaurante.mostrar_pedidos()},{direccion_cliente}")
        client_socket.sendall("Pedido enviado a cocina. Espere a ser llamado.".encode())
        print(f"Cliente {client_socket.getpeername()} - Pedido enviado a cocina: {restaurante.mostrar_pedidos()}")
        restaurante.pedidos.clear()

# --- Ahora la cocina se gestiona manualmente desde el servidor ---

def print_pedidos_en_cola(pedidos_queue):
    """Imprime los pedidos pendientes de la cola interna."""
    print(f"\n{Fore.CYAN}Pedidos para preparar:{Style.RESET_ALL}")
    with pedidos_queue.mutex:
        for i, pedido_detalle in enumerate(pedidos_queue.queue, start=1):
            if pedido_detalle is not None:
                print(f"{Fore.YELLOW}{i}: {pedido_detalle}{Style.RESET_ALL}")

def mostrar_menu_cocina():
    """Muestra el menú de opciones para la cocina interna."""
    print(f"\n{Fore.MAGENTA}Opciones de cocina:{Style.RESET_ALL}")
    print(f"1. {Fore.CYAN}Ver pedidos actuales{Style.RESET_ALL}")
    print(f"2. {Fore.CYAN}Marcar pedido como finalizado manualmente{Style.RESET_ALL}")
    print(f"3. {Fore.CYAN}Salir del menú de cocina{Style.RESET_ALL}")

def marcar_pedido_como_finalizado_manualmente(pedidos_queue):
    """Marca un pedido como finalizado manualmente y envía una confirmación al cliente."""
    pedido_a_finalizar = input(f"{Fore.YELLOW}Ingrese el número del pedido ya finalizado: {Style.RESET_ALL}").strip()
    with pedidos_queue.mutex:
        try:
            pedido_num = int(pedido_a_finalizar) - 1
            if 0 <= pedido_num < len(pedidos_queue.queue):
                pedido_finalizado = pedidos_queue.queue[pedido_num]
                if pedido_finalizado is not None:
                    pedidos_queue.queue[pedido_num] = None
                    print(f"{Fore.GREEN}Pedido '{pedido_num + 1}' marcado como finalizado manualmente.{Style.RESET_ALL}")
                    # Extraer la dirección del cliente
                    partes = pedido_finalizado.rsplit(",", 1)
                    direccion_cliente = partes[-1].strip()
                    if direccion_cliente in clientes_sockets:
                        cliente_socket, _ = clientes_sockets[direccion_cliente]
                        cliente_socket.sendall("Pedido listo para retirar (finalizado manualmente)".encode())
                        print(f"{Fore.GREEN}Notificación enviada al cliente {direccion_cliente}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}El pedido ya fue finalizado o no existe.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Pedido '{pedido_a_finalizar}' no encontrado o ya finalizado.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Número de pedido no válido. Por favor, ingrese un número.{Style.RESET_ALL}")

def manage_pedidos_local(pedidos_queue):
    """Gestiona los pedidos desde la propia consola del servidor (opcional)."""
    while True:
        mostrar_menu_cocina()
        opcion = input(f"{Fore.GREEN}Seleccione una opción:{Style.RESET_ALL} ")
        if opcion == "1":
            print_pedidos_en_cola(pedidos_queue)
        elif opcion == "2":
            marcar_pedido_como_finalizado_manualmente(pedidos_queue)
        elif opcion == "3":
            print(f"{Fore.RED}Saliendo de la interfaz de cocina interna...{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Opción no válida. Por favor, intente de nuevo.{Style.RESET_ALL}")

def aceptar_conexiones(server_socket):
    """Función para aceptar conexiones en un socket de servidor en un hilo separado."""
    while True:
        conn, addr = server_socket.accept()
        direccion_cliente_formateada = f"{addr[0]}:{addr[1]}"
        imprimir_mensaje(f"Conexión aceptada desde {direccion_cliente_formateada}", 'SUCCESS')
        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()

def server():
    """Inicia el servidor."""
    PORT = 50007
    server_sockets = []

    # Obtener información de todas las interfaces disponibles (IPv4 e IPv6)
    try:
        direcciones = socket.getaddrinfo(None, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
    except socket.gaierror as e:
        imprimir_mensaje(f"Error al obtener información de interfaces: {e}", 'ERROR')
        logging.error(f"Error al obtener información de interfaces: {e}")
        return

    # Crear y vincular sockets para todas las direcciones obtenidas
    for direccion in direcciones:
        familia, tipo, proto, canonico, sockaddr = direccion
        try:
            server_socket = socket.socket(familia, tipo, proto)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            imprimir_mensaje(f"Servidor escuchando en {sockaddr[0]}:{sockaddr[1]}", 'SUCCESS')
            server_socket.bind(sockaddr)
            server_socket.listen(5)
            server_sockets.append(server_socket)
        except OSError as e:
            imprimir_mensaje(f"Error al crear o vincular socket en {sockaddr[0]}:{sockaddr[1]} - {e}", 'ERROR')
            logging.error(f"Error al crear o vincular socket en {sockaddr[0]}:{sockaddr[1]} - {e}")

    if not server_sockets:
        imprimir_mensaje("No se pudo crear ningún socket para las direcciones especificadas", 'ERROR')
        return

    # Ya no iniciamos el hilo de cocina_interna, porque ahora la finalización es sólo manual.
    # Iniciar menú interno de cocina (opcional)
    interfaz_cocina_thread = threading.Thread(target=manage_pedidos_local, args=(pedidos_queue,), daemon=True)
    interfaz_cocina_thread.start()

    # Crear e iniciar un hilo para aceptar conexiones en cada socket del servidor
    for server_socket in server_sockets:
        server_thread = threading.Thread(target=aceptar_conexiones, args=(server_socket,))
        server_thread.start()

# Iniciar el servidor
if __name__ == "__main__":
    server()
