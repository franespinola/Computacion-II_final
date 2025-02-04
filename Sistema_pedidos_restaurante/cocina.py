import threading
from colorama import Fore, Style
from servidor import pedidos_queue, clientes_sockets, imprimir_mensaje
# Podrías importar logging si lo necesitas

pedidos_en_cocina = []  # lista local donde almacenamos pedidos

def cocina_interna():
    """
    Hilo que consume pedidos desde pedidos_queue con get().
    Cada pedido que extrae, lo guarda en pedidos_en_cocina
    para poder marcarlo manualmente.
    """
    while True:
        pedido = pedidos_queue.get()  # bloquea hasta que haya un pedido
        if pedido is None:
            break  
        pedidos_en_cocina.append(pedido)
        imprimir_mensaje(f"Pedido recibido en cocina: {pedido}", 'INFO')

def mostrar_menu_cocina():
    print(f"\n{Fore.MAGENTA}Opciones de cocina:{Style.RESET_ALL}")
    print("1. Ver pedidos actuales")
    print("2. Marcar pedido como finalizado manualmente")
    print("3. Salir del menú de cocina")

def print_pedidos_en_cola_local():
    if not pedidos_en_cocina:
        print("No hay pedidos en la cocina.")
        return
    print(f"\n{Fore.CYAN}Pedidos en cocina (no finalizados):{Style.RESET_ALL}")
    for i, pedido in enumerate(pedidos_en_cocina, start=1):
        print(f"{i}. {pedido}")

def marcar_pedido_finalizado():
    if not pedidos_en_cocina:
        print("No hay pedidos en la cocina.")
        return
    idx_str = input("Ingrese el número del pedido a finalizar: ").strip()
    try:
        idx = int(idx_str) - 1
    except ValueError:
        print("Debe ingresar un número.")
        return
    if idx < 0 or idx >= len(pedidos_en_cocina):
        print("Índice fuera de rango.")
        return
    pedido_finalizado = pedidos_en_cocina.pop(idx)
    
    # Extraer la dirección del cliente para notificarlo
    partes = pedido_finalizado.rsplit(",", 1)
    direccion_cliente = partes[-1].strip()
    print(f"Pedido '{idx_str}' marcado como finalizado.")

    # Notificar al cliente, si está conectado
    if direccion_cliente in clientes_sockets:
        cliente_socket, _ = clientes_sockets[direccion_cliente]      #guardo solo la direccion del cliente(por eso el _ para omitir lo otro)
        try:
            cliente_socket.sendall("Pedido listo para retirar".encode())
            print(f"Notificación enviada al cliente {direccion_cliente}")
        except Exception as e:
            print(f"Error al notificar al cliente {direccion_cliente}: {e}")
    else:
        print(f"No se encontró cliente para {direccion_cliente} (posiblemente se desconectó).")

def manage_pedidos_local():
    """
    Menú interactivo para la cocina (bloquea el hilo principal o de donde se lo llame).
    """
    while True:
        mostrar_menu_cocina()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            print_pedidos_en_cola_local()
        elif opcion == "2":
            marcar_pedido_finalizado()
        elif opcion == "3":
            print("Saliendo del menú de cocina...")
            break
        else:
            print("Opción no válida.")

def iniciar_cocina():
    """
    Inicia el hilo que consume pedidos de la cola (cocina_interna)
    y lanza el menú local manage_pedidos_local().
    """
    hilo_cocina = threading.Thread(target=cocina_interna, daemon=True)
    hilo_cocina.start()

    # El menú se ejecuta en el hilo principal
    manage_pedidos_local()
