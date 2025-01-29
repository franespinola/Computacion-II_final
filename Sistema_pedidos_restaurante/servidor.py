import socket
import threading
import queue
from collections import defaultdict
from colorama import Fore, Style
import logging
import time

from carta import carta
from restaurante import Restaurante

# Configuración de logging
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

# Diccionario para almacenar los sockets de los clientes
clientes_sockets = {}

# Cola de pedidos (productores: 'enviar_pedido_a_cocina_y_salir', consumidor: 'cocina_interna')
pedidos_queue = queue.Queue()

# Lista local donde la cocina mantiene los pedidos recibidos pero no finalizados
pedidos_en_cocina = []

##################################################################
#                         LÓGICA SERVIDOR
##################################################################

def handle_client(client_socket):
    """Maneja la conexión con un cliente."""
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

        imprimir_mensaje(f"Opción recibida: {opcion} (Cliente: {cliente_id})", 'INFO')

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
    logging.info(f"Cliente {client_socket.getpeername()} - Carta mostrada.")

def tomar_pedido(client_socket, restaurante):
    resp = f"{Fore.GREEN}Tomando pedido...{Style.RESET_ALL}"
    client_socket.sendall(resp.encode())

    nombre = client_socket.recv(1024).decode()
    producto_id = int(client_socket.recv(1024).decode())
    cantidad = int(client_socket.recv(1024).decode())
    observaciones = client_socket.recv(1024).decode()

    producto = next((p for p in carta if p.id == producto_id), None)
    if producto:
        restaurante.tomar_pedido(nombre, producto, cantidad, observaciones)
        client_socket.sendall("Pedido tomado con éxito.".encode())
        logging.info(f"Cliente {client_socket.getpeername()} - Pedido tomado: {restaurante.pedidos[-1]}")
    else:
        logging.error(f"Cliente {client_socket.getpeername()} - Error: Producto no encontrado.")
        client_socket.sendall("Error: Producto no encontrado en la carta.".encode())

def mostrar_pedido(client_socket, restaurante):
    pedidos = restaurante.mostrar_pedidos()
    client_socket.sendall(pedidos.encode())
    if pedidos == "No hay pedidos.":
        return
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
            logging.error(f"Cliente {client_socket.getpeername()} - Error: Producto no encontrado.")
            client_socket.sendall("Error: Producto no encontrado en la carta.".encode())

def modificar_pedido(client_socket, restaurante):
    if restaurante.mostrar_pedidos() == "No hay pedidos.":
        client_socket.sendall("No hay pedidos.".encode())
        return

    client_socket.sendall(f"{Fore.YELLOW}Modificando pedido...{Style.RESET_ALL}".encode())
    id_pedido = int(client_socket.recv(1024).decode())
    if not restaurante.pedido_existe(id_pedido):
        msg = "El pedido con el ID proporcionado no existe."
        client_socket.sendall(msg.encode())
        logging.error(f"Cliente {client_socket.getpeername()} - {msg}")
    else:
        logging.info(f"Cliente {client_socket.getpeername()} - Pedido modificado: {id_pedido}")
        client_socket.sendall("Pedido modificado con éxito.".encode())

        producto_id = int(client_socket.recv(1024).decode())
        cantidad = int(client_socket.recv(1024).decode())
        observaciones = client_socket.recv(1024).decode()

        producto = next((p for p in carta if p.id == producto_id), None)
        if producto:
            result = restaurante.modificar_pedido(id_pedido, producto, cantidad, observaciones)
            client_socket.sendall(result.encode())
        else:
            logging.error("Producto no encontrado en la carta.")
            client_socket.sendall("Error: Producto no encontrado en la carta.".encode())

def eliminar_pedido(client_socket, restaurante):
    if restaurante.mostrar_pedidos() == "No hay pedidos.":
        client_socket.sendall("No hay pedidos.".encode())
        return

    msg = f"{Fore.RED}Eliminando pedido.....{Style.RESET_ALL}"
    client_socket.sendall(msg.encode())
    id_pedido = client_socket.recv(1024).decode()
    if not restaurante.pedido_existe(id_pedido):
        err = "El pedido con el ID proporcionado no existe."
        logging.error(f"Cliente {client_socket.getpeername()} - {err}")
        client_socket.sendall(err.encode())
    else:
        logging.info(f"Cliente {client_socket.getpeername()} - Pedido eliminado: {id_pedido}")
        restaurante.eliminar_pedido(id_pedido)
        client_socket.sendall("Pedido eliminado con éxito.".encode())
        print(f"Cliente {client_socket.getpeername()} - Pedido eliminado: {id_pedido}")

def enviar_pedido_a_cocina_y_salir(client_socket, restaurante):
    pedidos = restaurante.mostrar_pedidos()
    client_socket.sendall(pedidos.encode())
    if pedidos == "No hay pedidos.":
        return

    pregunta = client_socket.recv(1024).decode()
    if pregunta.lower() == 's':
        logging.info(f"Cliente {client_socket.getpeername()} - Pedido enviado a cocina")
        # Se pone en la cola
        direccion_cliente = f"{client_socket.getpeername()[0]}:{client_socket.getpeername()[1]}"
        pedidos_queue.put(f"{restaurante.mostrar_pedidos()},{direccion_cliente}")

        client_socket.sendall("Pedido enviado a cocina. Espere a ser llamado.".encode())
        print(f"Cliente {client_socket.getpeername()} - Pedido enviado a cocina: {restaurante.mostrar_pedidos()}")

        restaurante.pedidos.clear()

def aceptar_conexiones(server_socket):
    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()

def server():
    PORT = 50007
    server_sockets = []

    # Obtener información de interfaces
    direcciones = socket.getaddrinfo(None, PORT, socket.AF_UNSPEC,
                                     socket.SOCK_STREAM, 0, socket.AI_PASSIVE)

    for fam, tipo, proto, cname, sockaddr in direcciones:
        try:
            sock = socket.socket(fam, tipo, proto)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(sockaddr)
            sock.listen(5)
            imprimir_mensaje(f"Servidor escuchando en {sockaddr}", 'SUCCESS')
            server_sockets.append(sock)
        except OSError as e:
            imprimir_mensaje(f"Error al crear socket en {sockaddr}: {e}", 'ERROR')

    for s in server_sockets:
        threading.Thread(target=aceptar_conexiones, args=(s,), daemon=True).start()


##################################################################
#                    LÓGICA DE COCINA CON queue.get()
##################################################################

def cocina_interna():
    """
    Hilo consumidor clásico.
    Extrae pedidos de `pedidos_queue` con get(), 
    los guarda en `pedidos_en_cocina` para su posterior finalización manual.
    """
    while True:
        pedido = pedidos_queue.get()  # bloquea hasta que haya un pedido
        if pedido is None:
            break  # para terminar, si en algún momento quisieras terminar el hilo con 'put(None)'

        # Aquí 'pedido' es algo como "descripcion...,direccion_cliente"
        # Lo guardamos en la lista local
        pedidos_en_cocina.append(pedido)
        imprimir_mensaje(f"Pedido recibido: {pedido} (cocina_interna)", 'INFO')


def manage_pedidos_local():
    """
    Menú local para la cocina. 
    Opera sobre la lista 'pedidos_en_cocina' en lugar de la cola directamente.
    """
    while True:
        mostrar_menu_cocina()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            print_pedidos_en_cola()   # revisa la lista local
        elif opcion == "2":
            marcar_pedido_como_finalizado_manualmente()
        elif opcion == "3":
            print("Saliendo de la interfaz de cocina interna...")
            break
        else:
            print("Opción no válida.")


def mostrar_menu_cocina():
    print(f"\n{Fore.MAGENTA}Opciones de cocina:{Style.RESET_ALL}")
    print("1. Ver pedidos actuales")
    print("2. Marcar pedido como finalizado manualmente")
    print("3. Salir del menú de cocina")

def print_pedidos_en_cola():
    """Imprime los pedidos pendientes (de la lista local en cocina)."""
    print(f"\n{Fore.CYAN}Pedidos en cocina (no finalizados):{Style.RESET_ALL}")
    if not pedidos_en_cocina:
        print("No hay pedidos en la cocina.")
        return
    for i, pedido_detalle in enumerate(pedidos_en_cocina, start=1):
        print(f"{i}. {pedido_detalle}")

def marcar_pedido_como_finalizado_manualmente():
    if not pedidos_en_cocina:
        print("No hay pedidos en la cocina.")
        return
    
    index_str = input("Ingrese el número del pedido a finalizar: ").strip()
    try:
        idx = int(index_str) - 1
    except ValueError:
        print("Debe ingresar un número válido.")
        return
    
    if idx < 0 or idx >= len(pedidos_en_cocina):
        print("No existe el pedido.")
        return
    
    pedido_finalizado = pedidos_en_cocina[idx]
    # Extraemos la dirección del cliente
    partes = pedido_finalizado.rsplit(",", 1)
    direccion_cliente = partes[-1].strip()

    # Marcamos el pedido como finalizado, quitándolo de la lista local
    pedidos_en_cocina.pop(idx)

    print(f"Pedido '{index_str}' marcado como finalizado manualmente.")
    # Notificamos al cliente (si todavía está conectado)
    if direccion_cliente in clientes_sockets:
        cliente_socket, _ = clientes_sockets[direccion_cliente]
        try:
            cliente_socket.sendall("Pedido listo para retirar (finalizado manualmente)".encode())
            print(f"Notificación enviada al cliente {direccion_cliente}")
        except Exception as e:
            print(f"Error al notificar al cliente {direccion_cliente}: {e}")
    else:
        print(f"No se encontró cliente para la dirección {direccion_cliente}. Quizá se desconectó.")


##################################################################
#                 PUNTO DE ENTRADA
##################################################################

if __name__ == "__main__":
    # Iniciar el servidor en hilos
    server()

    # Iniciar el hilo consumidor que saca pedidos de la cola
    threading.Thread(target=cocina_interna, daemon=True).start()

    # Iniciar el menú interno de cocina en el hilo principal
    # (bloqueante, para simular la interfaz de consola)
    manage_pedidos_local()
