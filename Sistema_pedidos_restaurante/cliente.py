# Archivo cliente.py
import socket

def start_client(host, port):
    # Crea un socket TCP/IP
    client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    
    try:
        # Conecta el socket al servidor
        client_socket.connect((host, port))
        
        while True:
            # Envía un mensaje al servidor
            message = input("Introduce un mensaje para el servidor: ")
            client_socket.sendall(message.encode())
            print('Mensaje enviado al servidor:', message)
            
            # Recibe datos del servidor
            data = client_socket.recv(1024)
            print('Mensaje recibido del servidor:', data.decode())
        
    except ConnectionRefusedError:
        print("[!] No se pudo conectar al servidor.")
    except socket.error as e:
        print(f"[!] Error de socket: {e}")
    except KeyboardInterrupt:
        print("\n[!] Keyboard Interrupt.")
    finally:
        # Cierra la conexión
        print("Closing client.")
        client_socket.close()

if __name__ == "__main__":
    start_client('::1', 9999)  # Puedes configurar el host y el puerto aquí


