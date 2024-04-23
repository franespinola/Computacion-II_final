# servidor.py

import socket
import threading
from producto import Producto
from restaurante import Restaurante


carta = [
    Producto(1, "Hamburguesa", 12.50, "Plato principal", "Carne, queso, tomate, lechuga."),
    Producto(2, "Papas fritas", 3.50, "Guarnición", "Papas fritas cortadas en juliana."),
    Producto(3, "Coca-Cola", 2.50, "Bebida", "Refresco de cola."),
]

restaurante = Restaurante(carta)

def handle_client(client_socket):
    while True:
        # Recibir la elección del cliente
        data = client_socket.recv(1024)
        if not data:
            break
        opcion = data.decode()
        if opcion == "1":
            respuesta = restaurante.mostrar_carta()
        elif opcion == "2":
            respuesta = restaurante.tomar_pedido()
        elif opcion == "3":
            respuesta = restaurante.mostrar_pedidos()
        elif opcion == "4":
            respuesta = "Saliendo del programa."
            client_socket.sendall(respuesta.encode())
            break
        else:
            respuesta = "Opción no válida."
        client_socket.sendall(respuesta.encode())

def server_loop():
    HOST = 'localhost'
    PORT = 50007
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()

server_loop()


    


