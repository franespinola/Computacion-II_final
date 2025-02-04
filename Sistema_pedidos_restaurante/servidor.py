import socket
import threading
import logging
from collections import defaultdict
from colorama import Fore, Style
from carta import carta
from restaurante import Restaurante
import queue

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
    """Maneja la comunicación con un cliente (un hilo por cliente)."""
    restaurante = Restaurante(carta)
    direccion_cliente = client_socket.getpeername()
    cliente_id = f"{direccion_cliente[0]}:{direccion_cliente[1]}"
    clientes_sockets[cliente_id] = (client_socket, restaurante)
    imprimir_mensaje(f"Conexión establecida con {cliente_id}", 'SUCCESS')
    logging.info(f"Conexión establecida con {cliente_id}")

    while True:
        opcion = client_socket.recv(1024).decode().strip()
        if not opcion:
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
            enviar_pedido_a_cocina_y_salir(client_socket, restaurante)

    client_socket.close()
    del clientes_sockets[cliente_id]
    imprimir_mensaje(f"Conexión cerrada y recursos liberados para {cliente_id}", 'INFO')
    logging.info(f"Conexión cerrada y recursos liberados para {cliente_id}")

def mostrar_carta(client_socket):
    productos_por_categoria = defaultdict(list)
    for producto in carta:
        productos_por_categoria[producto.categoria].append(producto)

    respuesta = ""
    for categoria, productos in productos_por_categoria.items():
        respuesta += f"\n\n{Fore.GREEN}{categoria}{Style.RESET_ALL}:\n"
        for p in productos:
            respuesta += f"{p}\n"
    client_socket.sendall(respuesta.encode())

def tomar_pedido(client_socket, restaurante):
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

def mostrar_pedido(client_socket, restaurante):
    pedidos = restaurante.mostrar_pedidos()
    client_socket.sendall(pedidos.encode())
    if pedidos == "No hay pedidos.":
        return
    else:
        pregunta = client_socket.recv(1024).decode()
        if pregunta.lower() == 's':
            nombre = client_socket.recv(1024).decode()
            producto_id = int(client_socket.recv(1024).decode())
            cantidad = int(client_socket.recv(1024).decode())
            observaciones = client_socket.recv(1024).decode()
            producto = next((p for p in carta if p.id == producto_id), None)
            if producto:
                restaurante.tomar_pedido(nombre, producto, cantidad, observaciones)
                client_socket.sendall(restaurante.mostrar_pedidos().encode())
            else:
                client_socket.sendall("Error: Producto no encontrado en la carta.".encode())

def modificar_pedido(client_socket, restaurante):
    if restaurante.mostrar_pedidos() == "No hay pedidos.":
        client_socket.sendall("No hay pedidos.".encode())
        return
    client_socket.sendall("Modificando pedido...".encode())

    id_pedido = int(client_socket.recv(1024).decode())
    if not restaurante.pedido_existe(id_pedido):
        client_socket.sendall("El pedido con el ID proporcionado no existe.".encode())
    else:
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

def eliminar_pedido(client_socket, restaurante):
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

def enviar_pedido_a_cocina_y_salir(client_socket, restaurante):
    pedidos = restaurante.mostrar_pedidos()
    client_socket.sendall(pedidos.encode())
    if pedidos == "No hay pedidos.":
        return

    pregunta = client_socket.recv(1024).decode()
    if pregunta.lower() == 's':
        direccion_cliente = f"{client_socket.getpeername()[0]}:{client_socket.getpeername()[1]}"
        # Insertar en la cola
        pedidos_queue.put(f"{restaurante.mostrar_pedidos()},{direccion_cliente}")
        client_socket.sendall("Pedido enviado a cocina. Espere a ser llamado.".encode())
        restaurante.pedidos.clear()

def aceptar_conexiones(server_socket):
    while True:
        conn, addr = server_socket.accept()
        imprimir_mensaje(f"Conexión aceptada desde {addr}", 'SUCCESS')
        hilo_cliente = threading.Thread(target=handle_client, args=(conn,))
        hilo_cliente.start()

def server():
    PORT = 50007
    server_sockets = []

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

    # Iniciar un hilo por cada socket
    for sock in server_sockets:
        hilo = threading.Thread(target=aceptar_conexiones, args=(sock,), daemon=True)
        hilo.start()
