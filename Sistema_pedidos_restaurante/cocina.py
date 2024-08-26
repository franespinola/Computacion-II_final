import socket
import threading
import queue
from colorama import Fore, Style

def handle_kitchen(client_socket, pedidos_queue):
    """Maneja la conexión con el servidor y agrega los pedidos a la cola."""
    while True:
        pedido = client_socket.recv(1024).decode().strip()
        if not pedido:
            break
        
        pedidos_queue.put(pedido)
        print(f"\n{Fore.GREEN}Nuevo pedido recibido:{Style.RESET_ALL}")
        print_pedidos(pedidos_queue)
        
    client_socket.close()

def print_pedidos(pedidos_queue):
    """Imprime los pedidos pendientes de la cola."""
    print(f"\n{Fore.CYAN}Pedidos para preparar:{Style.RESET_ALL}")
    with pedidos_queue.mutex:
        for i, pedido_detalle in enumerate(pedidos_queue.queue, start=1):
            if pedido_detalle is not None:
                print(f"{Fore.YELLOW}{i}: {pedido_detalle}{Style.RESET_ALL}")

def enviar_confirmacion_al_servidor(confirmacion):
    """Envía una confirmación al servidor."""
    cocina_host = 'localhost'
    cocina_port = 50009  # Nuevo puerto para la comunicación con el servidor
    cocina_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cocina_socket.connect((cocina_host, cocina_port))
        cocina_socket.sendall(confirmacion.encode())
    finally:
        cocina_socket.close()

def manage_pedidos(pedidos_queue):
    """Gestiona los pedidos a través de un menú interactivo."""
    while True:
        mostrar_menu_cocina()
        opcion = input(f"{Fore.GREEN}Seleccione una opción:{Style.RESET_ALL} ")

        if opcion == "1":
            print_pedidos(pedidos_queue)
        elif opcion == "2":
            marcar_pedido_como_finalizado(pedidos_queue)
        elif opcion == "3":
            print(f"{Fore.RED}Saliendo...{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Opción no válida. Por favor, intente de nuevo.{Style.RESET_ALL}")

def mostrar_menu_cocina():
    """Muestra el menú de opciones para la cocina."""
    print(f"\n{Fore.MAGENTA}Opciones:{Style.RESET_ALL}")
    print(f"1. {Fore.CYAN}Ver pedidos actuales{Style.RESET_ALL}")
    print(f"2. {Fore.CYAN}Marcar pedido como finalizado{Style.RESET_ALL}")
    print(f"3. {Fore.CYAN}Salir{Style.RESET_ALL}")

def marcar_pedido_como_finalizado(pedidos_queue):
    """Marca un pedido como finalizado y envía una confirmación al servidor."""
    pedido_a_finalizar = input(f"{Fore.YELLOW}Ingrese el número del pedido ya finalizado: {Style.RESET_ALL}").strip()
    with pedidos_queue.mutex:
        try:
            pedido_num = int(pedido_a_finalizar) - 1
            if 0 <= pedido_num < len(pedidos_queue.queue):
                pedido_finalizado = pedidos_queue.queue[pedido_num]
                pedidos_queue.queue[pedido_num] = None
                print(f"{Fore.GREEN}Pedido '{pedido_num + 1}' marcado como finalizado.{Style.RESET_ALL}")
                
                if pedido_finalizado:
                    # Incluye el ID del pedido en la confirmación
                    enviar_confirmacion_al_servidor(f"LISTO {pedido_finalizado}")
                    print(f"{Fore.GREEN}Confirmación de pedido '{pedido_finalizado}' enviada al servidor.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Pedido '{pedido_a_finalizar}' no encontrado o ya finalizado.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Número de pedido no válido. Por favor, ingrese un número.{Style.RESET_ALL}")

def cocina():
    """Función principal de la cocina."""
    HOST = 'localhost'
    PORT = 50008
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"{Fore.GREEN}Cocina lista y esperando pedidos...{Style.RESET_ALL}")

    pedidos_queue = queue.Queue()

    threading.Thread(target=manage_pedidos, args=(pedidos_queue,), daemon=True).start()

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_kitchen, args=(conn, pedidos_queue)).start()

if __name__ == "__main__":
    cocina()
