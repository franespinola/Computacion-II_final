import socket
import threading
from restaurante import Restaurante
from menus import carta

restaurante = Restaurante(carta) #tengo que pasar la carta como parametro

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
        else:
            respuesta = "Opción no válida."
        client_socket.sendall(respuesta.encode())

def server_loop():
    HOST = 'localhost'
    PORT = 50007
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)

    try:
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn,))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nSaliendo del programa.")
server_loop()


    


