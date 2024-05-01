import socket
import threading
from carta import carta
from pedido import Pedido
from collections import defaultdict
from colorama import Fore, Style

def handle_client(client_socket):

    while True:

        data = client_socket.recv(1024) #aca viene los datos en bytes(mas abajo los transformo a string)
        print("Data recibida:", data) 
        if not data:
            break
        opcion = data.decode()  #hago la decodificacion de los datos con decode
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

    #-------------Tomar pedido---------------------------------------- # 
        elif opcion == "2":
            respuesta = "Tomando pedido."
            client_socket.sendall(respuesta.encode())
            nombre = client_socket.recv(1024).decode() # Recibir el nombre del cliente
            producto = client_socket.recv(1024).decode() # Recibir el producto
            cantidad = client_socket.recv(1024).decode() # Recibir la cantidad
            observaciones = client_socket.recv(1024).decode() # Recibir las observaciones
            pedido=Pedido(nombre, producto, cantidad, observaciones) # Crear un pedido con los datos recibidos
            print(pedido)
        
    #-------------Mostrar pedido---------------------------------------- #     
        elif opcion == "3":
            respuesta = "Mostrando pedidos."
        
        elif opcion == "4":
            respuesta = "Saliendo del programa."
        
        else:
            respuesta = "Opción no válida."
        client_socket.sendall(respuesta.encode())

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






    


