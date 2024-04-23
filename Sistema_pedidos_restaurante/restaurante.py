# restaurante.py

from pedido import Pedido
from cocina import Cocina

class Restaurante:
    def __init__(self, carta):
        self.carta = carta
        self.pedidos = []
        self.cocina = Cocina()

    def mostrar_carta(self):
        carta_str = '\n'.join(str(producto) for producto in self.carta)
        return carta_str

    def tomar_pedido(self):
        pedido_id = len(self.pedidos) + 1
        cliente = input("Nombre del cliente: ")
        mesa = int(input("Número de mesa: "))

        nuevo_pedido = Pedido(pedido_id, cliente, mesa)

        print("\nMostrando carta:")
        self.mostrar_carta()

        while True:
            id_producto = int(input("Ingrese ID del producto a agregar: "))
            cantidad = int(input("Ingrese cantidad: "))
            observaciones = input("Observaciones (opcional): ")

            producto = next((p for p in self.carta if p.id == id_producto), None)

            if producto:
                nuevo_pedido.agregar_item(producto, cantidad, observaciones)
                print(f"Producto {producto.nombre} agregado al pedido.")
                continuar = input("¿Desea agregar otro producto? (s/n): ")
                if continuar.lower() != "s":
                    break
            else:
                print(f"Producto con ID {id_producto} no encontrado.")

        nuevo_pedido.calcular_total()
        print(f"\nResumen del pedido:\n{nuevo_pedido}")

        confirmar_pedido = input("¿Confirmar pedido? (s/n): ")
        if confirmar_pedido.lower() == "s":
            nuevo_pedido.enviar_a_cocina()
            self.pedidos.append(nuevo_pedido)
            print("Pedido enviado a cocina.")
        else:
            print("Pedido cancelado.")

    def mostrar_pedidos(self):
        if not self.pedidos:
            print("No hay pedidos en curso o listos.")
            return

        print("\nPedidos en curso:")
        for pedido in self.pedidos:
            if pedido.estado == "En curso":
                print(f"{pedido.id}: {pedido.cliente} ({pedido.mesa})")

        print("\nPedidos listos:")
        for pedido in self.pedidos:
            if pedido.estado == "Listo":
                print(f"{pedido.id}: {pedido.cliente} ({pedido.mesa})")
