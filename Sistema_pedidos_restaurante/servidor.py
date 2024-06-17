import socket
import threading
from carta import carta
from restaurante import Restaurante
from collections import defaultdict
from colorama import Fore, Style
import logging

# Configuración del logging
logging.basicConfig(filename='servidor.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s') 

cliente_pedidos = {}  # Diccionario para almacenar pedidos por cliente

def handle_client(client_socket):
    restaurante = Restaurante(carta)
    print(f"Conexión establecida con el cliente {client_socket.getpeername()}")
    while True:
        try:
            opcion = client_socket.recv(1024).decode()
            print(f"Opción recibida: {opcion}, Cliente: {client_socket.getpeername()}")

            if opcion == "1":
                productos_por_categoria = defaultdict(list)
                respuesta = ""
                for producto in carta:
                    productos_por_categoria[producto.categoria].append(producto)
                for categoria in productos_por_categoria:
                    respuesta += f"\n\n{Fore.GREEN}{categoria}{Style.RESET_ALL}:\n\n"
                    respuesta += "\n".join(str(producto) for producto in productos_por_categoria[categoria])
                client_socket.sendall(respuesta.encode())
                logging.info(f"Cliente {client_socket.getpeername()} - Carta mostrada.") 

            elif opcion == "2":
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
                    cliente_pedidos[client_socket.getsockname()] = restaurante.pedidos[-1]  # Asociar el pedido al cliente
                else:
                    logging.error(f"Cliente {client_socket.getpeername()} - Error: Producto no encontrado en la carta.")
                    client_socket.sendall("Error: Producto no encontrado en la carta.".encode())

            elif opcion == "3":
                client_socket.sendall(restaurante.mostrar_pedidos().encode())
                if restaurante.mostrar_pedidos() == "No hay pedidos.":
                    logging.info(f"Cliente {client_socket.getpeername()} - No hay pedidos.")
                    continue
                else:
                    logging.info(f"Cliente {client_socket.getpeername()} - Pedidos mostrados")
                pregunta = client_socket.recv(1024).decode()
                if pregunta.lower() == 's':
                    producto_id = int(client_socket.recv(1024).decode())
                    cantidad = int(client_socket.recv(1024).decode())
                    observaciones = client_socket.recv(1024).decode()
                    producto = next((prod for prod in carta if prod.id == producto_id), None)
                    if producto is not None:
                        restaurante.tomar_pedido(nombre, producto, cantidad, observaciones)
                        cliente_pedidos[client_socket.getsockname()] = restaurante.pedidos[-1] 
                    else:
                        logging.error(f"Cliente {client_socket.getpeername()} - Error: Producto no encontrado en la carta.")
                        client_socket.sendall("Error: Producto no encontrado en la carta.".encode())
                    client_socket.sendall(restaurante.mostrar_pedidos().encode())
        
            elif opcion == "4":
                if restaurante.mostrar_pedidos() == "No hay pedidos.":
                    client_socket.sendall("No hay pedidos.".encode())
                    continue
                mensaje = f"{Fore.YELLOW}Modificando pedido...{Style.RESET_ALL}"
                client_socket.sendall(mensaje.encode())
                id_pedido = int(client_socket.recv(1024).decode())
                if not restaurante.pedido_existe(id_pedido):
                    client_socket.sendall("El pedido con el ID proporcionado no existe.".encode())
                    logging.error(f"Cliente {client_socket.getpeername()} - Error: Pedido no encontrado para su modificacion.")
                else:
                    logging.info(f"Cliente {client_socket.getpeername()} - Pedido modificado: {id_pedido}")
                    client_socket.sendall("Pedido modificado con éxito.".encode())
                    producto_id = int(client_socket.recv(1024).decode())
                    cantidad = int(client_socket.recv(1024).decode())
                    observaciones = client_socket.recv(1024).decode()
                    producto = next((prod for prod in carta if prod.id == producto_id), None)
                    if producto is not None:
                        client_socket.sendall(restaurante.modificar_pedido(id_pedido, producto, cantidad, observaciones).encode())
                        cliente_pedidos[client_socket.getsockname()] = restaurante.pedidos[id_pedido - 1] 
                    else:
                        logging.error(f"Cliente {client_socket.getpeername()} - Error: Producto no encontrado en la carta.")
                        client_socket.sendall("Error: Producto no encontrado en la carta.".encode())

            elif opcion == "5":
                if restaurante.mostrar_pedidos() == "No hay pedidos.":
                    client_socket.sendall("No hay pedidos.".encode())
                    continue
                mensaje = f"{Fore.RED}Eliminando pedido.....{Style.RESET_ALL}"
                client_socket.sendall(mensaje.encode())
                id_pedido = client_socket.recv(1024).decode()
                if not restaurante.pedido_existe(id_pedido):
                    logging.error(f"Cliente {client_socket.getpeername()} - Error: Pedido no encontrado para su eliminacion.")
                    client_socket.sendall("El pedido con el ID proporcionado no existe.".encode())
                else:
                    logging.info(f"Cliente {client_socket.getpeername()} - Pedido eliminado: {id_pedido}")
                    restaurante.eliminar_pedido(id_pedido)
                    client_socket.sendall("Pedido eliminado con éxito.".encode())
                    print(f"Cliente {client_socket.getpeername()} - Pedido eliminado: {id_pedido}")
                    del cliente_pedidos[client_socket.getsockname()]  # Eliminar el pedido del cliente
            
            elif opcion == "6":
                client_socket.sendall(restaurante.mostrar_pedidos().encode())
                if restaurante.mostrar_pedidos() == "No hay pedidos.":
                    continue
                pregunta = client_socket.recv(1024).decode()
                if pregunta.lower() == 's':
                    logging.info(f"Cliente {client_socket.getpeername()} - Pedido enviado a cocina")
                    client_socket.sendall("Pedido enviado a cocina. Espere a ser llamado.".encode())
                    enviar_a_cocina(restaurante.mostrar_pedidos(), client_socket)    
                    
        except ConnectionResetError:
            print(f"Cliente {client_socket.getpeername()} desconectado.")
            break  # Salir del bucle si el cliente se desconecta
        
def enviar_a_cocina(pedido, client_socket):
    try:
        cocina_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cocina_socket.connect(('localhost', 54321)) 
        print("Conexión establecida con la cocina")

        # Enviar el pedido y el socket del cliente a la cocina
        mensaje = f"{pedido}|{client_socket.getsockname()}" 
        cocina_socket.sendall(mensaje.encode('utf-8')) 

        print(f"Cliente {client_socket.getpeername()} - Pedido enviado a cocina: {pedido}")

        # Esperar la respuesta de la cocina
        respuesta_cocina = cocina_socket.recv(1024).decode('utf-8')
        print(f"Respuesta de la cocina: {respuesta_cocina}")

        # Enviar la respuesta de la cocina al cliente
        client_socket.sendall(respuesta_cocina.encode('utf-8'))

    except ConnectionRefusedError:
        print("No se pudo conectar a la cocina. Asegúrate de que esté en ejecución.")
    finally:
        cocina_socket.close()  

def server():
    HOST = 'localhost'
    PORT = 50007
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()

server()