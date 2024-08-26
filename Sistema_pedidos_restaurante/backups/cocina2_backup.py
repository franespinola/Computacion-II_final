import socket
import threading
import queue

def handle_kitchen(client_socket, pedidos_queue):
    while True:
        pedido = client_socket.recv(1024).decode().strip()
        if not pedido:
            break
        
        pedidos_queue.put(pedido)  # Añade el pedido a la cola
        print("\nNuevo pedido recibido:")
        print_pedidos(pedidos_queue)
        
    client_socket.close()

def print_pedidos(pedidos_queue):
    print("\nPedidos para preparar:")
    with pedidos_queue.mutex:  # Accede a la cola de manera segura
        for i, pedido_detalle in enumerate(pedidos_queue.queue, start=1):
            if pedido_detalle is not None:  # Solo imprime pedidos no finalizados
                print(f"{i}: {pedido_detalle}")

def enviar_confirmacion_al_servidor(confirmacion):
    cocina_host = 'localhost'
    cocina_port = 50007  # Puerto del servidor
    cocina_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cocina_socket.connect((cocina_host, cocina_port))
        cocina_socket.sendall(confirmacion.encode())
    finally:
        cocina_socket.close()

def manage_pedidos(pedidos_queue):
    while True:
        print("\nOpciones:")
        print("1. Ver pedidos actuales")
        print("2. Marcar pedido como finalizado")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print_pedidos(pedidos_queue)
        elif opcion == "2":
            pedido_a_finalizar = input("Ingrese el número del pedido ya finalizado: ").strip()
            with pedidos_queue.mutex:  # Accede a la cola de manera segura
                try:
                    pedido_num = int(pedido_a_finalizar) - 1  # Ajusta el índice para la lista
                    if 0 <= pedido_num < len(pedidos_queue.queue):
                        pedido_finalizado = pedidos_queue.queue[pedido_num]
                        pedidos_queue.queue[pedido_num] = None  # Marca el pedido como finalizado
                        print(f"Pedido '{pedido_num + 1}' marcado como finalizado.")
                        
                        # Enviar confirmación al servidor
                        if pedido_finalizado:
                            enviar_confirmacion_al_servidor("Pedido listo")
                            print(f"Confirmación de pedido '{pedido_finalizado}' enviada al servidor.")
                    else:
                        print(f"Pedido '{pedido_a_finalizar}' no encontrado o ya finalizado.")
                except ValueError:
                    print("Número de pedido no válido. Por favor, ingrese un número.")
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

def cocina():
    HOST = 'localhost'
    PORT = 50008
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print("Cocina lista y esperando pedidos...")

    pedidos_queue = queue.Queue()

    # Inicia el hilo que maneja el menú interactivo
    threading.Thread(target=manage_pedidos, args=(pedidos_queue,), daemon=True).start()

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_kitchen, args=(conn, pedidos_queue)).start()

if __name__ == "__main__":
    cocina()
