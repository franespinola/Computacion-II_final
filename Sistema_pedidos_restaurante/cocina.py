import socket
import threading

def handle_kitchen(client_socket):
    pedidos = []    
    while True:
        pedido = client_socket.recv(1024).decode()
        pedidos.append(pedido)
        if not pedido:
            break
        for i in range(len(pedidos)):
            print("Pedidos para preparar:")
            print(f"{pedidos[i]}")   
    client_socket.close()

def cocina():
    HOST = 'localhost'
    PORT = 50008
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print("Cocina lista y esperando pedidos...")

    while True:
        conn, addr = s.accept()
        kitchen_thread = threading.Thread(target=handle_kitchen, args=(conn,))
        kitchen_thread.start()

if __name__ == "__main__":
    cocina()
