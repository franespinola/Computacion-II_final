import socket
import threading
import sys

def handle_client(client_socket):
    # Maneja la conexión del cliente
    request = client_socket.recv(1024)
    print(f"[*] Received: {request.decode('utf-8')}")
    client_socket.send(b"ACK!")
    client_socket.close()

def start_server(host, port):
    # Crea un socket TCP/IP que acepta tanto IPv4 como IPv6
    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    
    # Permite reutilizar direcciones
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Asocia el socket al host y al puerto
    server_socket.bind((host, port))
    
    # Escucha conexiones entrantes
    server_socket.listen(5)  # Acepta hasta 5 conexiones pendientes
    
    print(f"[*] Listening on {host}:{port}")
    
    while True:
        # Acepta la conexión entrante
        client_socket, addr = server_socket.accept()
        
        # Inicia un nuevo hilo para manejar la conexión del cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server('::', 9999)  # Puedes configurar el host y el puerto aquí


