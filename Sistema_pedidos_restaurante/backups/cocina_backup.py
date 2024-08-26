import socket
import threading

def handle_kitchen(client_socket, pedidos, pedidos_lock):
    while True:
        pedido = client_socket.recv(1024).decode().strip()
        if not pedido:
            break
        
        with pedidos_lock:
            if pedido not in pedidos:
                pedido_id = len(pedidos) + 1  # Genera un ID único para el pedido
                pedidos[pedido_id] = pedido  # Asocia el ID con el detalle del pedido
                print("\nNuevo pedido recibido:")
                print_pedidos(pedidos)
    client_socket.close()

def print_pedidos(pedidos):
    print("\nPedidos para preparar:")
    for pedido_id, pedido_detalle in pedidos.items():
        if pedido_detalle is not None:  # Solo imprime pedidos no finalizados
            print(f"{pedido_id}: {pedido_detalle}")

def cocina():
    HOST = 'localhost'
    PORT = 50008
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print("Cocina lista y esperando pedidos...")

    pedidos = {}
    pedidos_lock = threading.Lock()

    def manage_pedidos():
        while True:
            print("\nOpciones:")
            print("1. Ver pedidos actuales")
            print("2. Marcar pedido como finalizado")
            print("3. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                with pedidos_lock:
                    print_pedidos(pedidos)
            elif opcion == "2":
                pedido_a_finalizar = input("Ingrese el ID del pedido ya finalizado: ").strip()
                with pedidos_lock:
                    try:
                        pedido_id = int(pedido_a_finalizar)
                        if pedido_id in pedidos and pedidos[pedido_id] is not None:
                            pedidos[pedido_id] = None  # Marca el pedido como finalizado
                            print(f"Pedido '{pedido_id}' marcado como finalizado.")
                        else:
                            print(f"Pedido '{pedido_id}' no encontrado o ya finalizado.")
                    except ValueError:
                        print("ID de pedido no válido. Por favor, ingrese un número.")
            elif opcion == "3":
                break
            else:
                print("Opción no válida. Por favor, intente de nuevo.")

    manager_thread = threading.Thread(target=manage_pedidos)
    manager_thread.daemon = True
    manager_thread.start()

    while True:
        conn, addr = s.accept()
        kitchen_thread = threading.Thread(target=handle_kitchen, args=(conn, pedidos, pedidos_lock))
        kitchen_thread.start()

if __name__ == "__main__":
    cocina()
