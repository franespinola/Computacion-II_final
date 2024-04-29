import socket
import pickle

HOST = 'localhost'
PORT = 50007

class Cliente:
    def mostrar_carta():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(pickle.dumps(("mostrar_carta", None)))
            data = s.recv(1024)
            carta = pickle.loads(data)
            print("Carta de productos:")
            for producto in carta:
                print(f"ID: {producto['id']} - {producto['nombre']} (${producto['precio']:.2f})")

    def tomar_pedido():
        cliente = input("Nombre del cliente: ")
        mesa = int(input("Número de mesa: "))
        detalles = []
        while True:
            id_producto = int(input("Ingrese ID del producto a agregar (0 para finalizar): "))
            if id_producto == 0:
                break
            cantidad = int(input("Ingrese cantidad: "))
            observaciones = input("Observaciones (opcional): ")
            detalles.append((id_producto, cantidad, observaciones))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(pickle.dumps(("tomar_pedido", (cliente, mesa, detalles))))
            data = s.recv(1024)
            print(data.decode())

    def mostrar_pedido():
        cliente = input("Nombre del cliente: ")
        mesa = int(input("Número de mesa: "))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(pickle.dumps(("mostrar_pedido", (cliente, mesa))))
            data = s.recv(1024)
            pedido = pickle.loads(data)
            print(f"Pedido de {cliente} en mesa {mesa}:")
            for producto in pedido:
                print(f"{producto['nombre']} x{producto['cantidad']} (${producto['precio']:.2f} c/u)")

    def modificar_pedido():
        cliente = input("Nombre del cliente: ")
        mesa = int(input("Número de mesa: "))
        detalles = []
        while True:
            id_producto = int(input("Ingrese ID del producto a modificar (0 para finalizar): "))
            if id_producto == 0:
                break
            cantidad = int(input("Ingrese cantidad: "))
            observaciones = input("Observaciones (opcional): ")
            detalles.append((id_producto, cantidad, observaciones))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(pickle.dumps(("modificar_pedido", (cliente, mesa, detalles))))
            data = s.recv(1024)
            print(data.decode())

    def eliminar_pedido():
        cliente = input("Nombre del cliente: ")
        mesa = int(input("Número de mesa: "))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(pickle.dumps(("eliminar_pedido", (cliente, mesa))))
            data = s.recv(1024)
            print(data.decode())

if __name__ == "__main__":
    while True:
        print("\nOpciones:")
        print("1. Mostrar carta")
        print("2. Tomar pedido")
        print("3. Modificar pedido")
        print("4. Eliminar pedido")
        print("5. Salir")
        opcion = input("Ingrese opción: ")
        if opcion == "1":
            Cliente.mostrar_carta()
        elif opcion == "2":
            Cliente.tomar_pedido()
        elif opcion == "3":
            Cliente.modificar_pedido()
        elif opcion == "4":
            Cliente.eliminar_pedido()
        elif opcion == "5":
            Cliente.mostrar_pedido()
        elif opcion == "6":
            break
        else:
            print("Opción no válida.")
