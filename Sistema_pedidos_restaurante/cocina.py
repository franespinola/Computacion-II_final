import socket

def iniciar_cocina():
    cocina_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cocina_socket.bind(('localhost', 54321))
    cocina_socket.listen(5)
    print("Cocina esperando pedidos del servidor...")

    while True:
        servidor_socket, servidor_direccion = cocina_socket.accept()
        print(f"Conexión establecida con el servidor: {servidor_direccion}")

        # Recibir pedido del servidor (incluyendo la información del cliente)
        pedido_completo = servidor_socket.recv(1024).decode('utf-8')
        pedido, cliente_addr = pedido_completo.split('|')

        print(f"Pedido recibido del servidor: {pedido}")
        print(f"Para el cliente: {cliente_addr}")

        # ... (lógica para procesar el pedido) ...

        # Simular que el cocinero preparó el pedido
        input("Presiona Enter cuando el pedido esté listo...")
        mensaje_listo = f"El pedido {pedido} está listo. ¡Buen provecho!"

        # Enviar la confirmación al servidor (incluyendo la información del cliente)
        servidor_socket.sendall(mensaje_listo.encode('utf-8'))
        
        servidor_socket.close()

if __name__ == "__main__":
    iniciar_cocina()