import socket
import threading

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        opcion = data.decode()             #traigo el numero que selecciono el cliente y hago la decodificacion ya que viene en bytes, lo transforma a string
        print("Opción recibida:", opcion)
        if opcion == "1":
            respuesta = "Mostrando carta."
        elif opcion == "2":
            respuesta = "Tomando pedido."
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






    


