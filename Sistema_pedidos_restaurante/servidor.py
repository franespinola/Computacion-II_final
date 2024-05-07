import socket
import threading
from carta import carta
from restaurante import Restaurante
from collections import defaultdict
from colorama import Fore, Style

def handle_client(client_socket):
    restaurante = Restaurante(carta) 
    while True:

        opcion = client_socket.recv(1024).decode()  #hago la decodificacion de los datos con decode. Recordando que vienen en bytes
        print("Opción recibida:", opcion)

    #-------------Mostrar carta---------------------------------------- #   
        if opcion == "1":
            productos_por_categoria = defaultdict(list) # Agrupar los productos por categoría
            respuesta = "" # Crear la respuesta
            for producto in carta:
                productos_por_categoria[producto.categoria].append(producto)
            for categoria in productos_por_categoria:
                respuesta += f"\n\n{Fore.GREEN}{categoria}{Style.RESET_ALL}:\n\n" # Agregar el título de la categoría
                respuesta += "\n".join(str(producto) for producto in productos_por_categoria[categoria]) # Agregar los productos de la categoría
            client_socket.sendall(respuesta.encode())

    #-------------Tomar pedido---------------------------------------- # 
        elif opcion == "2":
            respuesta = "Tomando pedido."
            client_socket.sendall(respuesta.encode())
            nombre = client_socket.recv(1024).decode() # Recibir el nombre del cliente
            producto = client_socket.recv(1024).decode() # Recibir el producto
            cantidad = client_socket.recv(1024).decode() # Recibir la cantidad
            observaciones = client_socket.recv(1024).decode() # Recibir las observaciones
            restaurante.tomar_pedido(nombre, producto, cantidad, observaciones)  # Tomar un pedido usando el método de Restaurante
            client_socket.sendall("Pedido tomado con éxito.".encode())

    #-------------Mostrar pedido---------------------------------------- #     
        elif opcion == "3":
            client_socket.sendall(restaurante.mostrar_pedidos().encode())
            pregunta = client_socket.recv(1024).decode()
            if pregunta.lower() == 's':
                producto = client_socket.recv(1024).decode()
                cantidad = client_socket.recv(1024).decode()
                restaurante.tomar_pedido(nombre, producto, cantidad, observaciones)  # Tomar un pedido usando el método de Restaurante
                client_socket.sendall(restaurante.mostrar_pedidos().encode())

    #-------------Modificar pedido---------------------------------------- #  
        elif opcion == "4":
            mensaje = f"{Fore.BLUE}Modificando pedido.{Style.RESET_ALL}"
            client_socket.sendall(mensaje.encode())
            id_pedido = client_socket.recv(1024).decode()
            if not restaurante.pedido_existe(id_pedido):
                client_socket.sendall("El pedido con el ID proporcionado no existe.".encode())
            else:
                client_socket.sendall("Pedido modificado con exito".encode())
                producto = client_socket.recv(1024).decode()
                cantidad = client_socket.recv(1024).decode()
                observaciones = client_socket.recv(1024).decode()
                client_socket.sendall(restaurante.modificar_pedido(id_pedido, producto, cantidad, observaciones).encode())

        #-------------Eliminar pedido---------------------------------------- # 
        elif opcion == "5":
            client_socket.sendall("Eliminando pedido.....".encode())
            id_pedido = client_socket.recv(1024).decode()
            if not restaurante.pedido_existe(id_pedido):
                client_socket.sendall("El pedido con el ID proporcionado no existe.".encode())
            else:
                restaurante.eliminar_pedido(id_pedido)
                client_socket.sendall("Pedido eliminado con éxito.".encode())



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






    


