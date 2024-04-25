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
        self.mostrar_carta()

        while True:
            print("\nOpciones:")
            print("1. Agregar producto al pedido")
            print("2. Eliminar producto del pedido")
            print("3. Modificar producto del pedido")
            print("4. Finalizar pedido")

            opcion = input("Ingrese opción: ")

            if opcion == "1": #agregar un producto al pedido
                id_producto = int(input("Ingrese ID del producto a agregar: "))
                cantidad = int(input("Ingrese cantidad: "))
                observaciones = input("Observaciones (opcional): ")

                producto = next((p for p in self.carta if p.id == id_producto), None)

                if producto:
                    nuevo_pedido.agregar_item(producto, cantidad, observaciones)
                    print(f"Producto {producto.nombre} agregado al pedido.")
                else:
                    print(f"Producto con ID {id_producto} no encontrado.")
            elif opcion == "2": #eliminar un producto del pedido
                id_producto = int(input("Ingrese ID del producto a eliminar: "))
                nuevo_pedido.eliminar_item(id_producto)
            elif opcion == "3": #modificar un producto del pedido
                id_producto = int(input("Ingrese ID del producto a modificar: "))
                cantidad = int(input("Ingrese nueva cantidad: "))
                observaciones = input("Nuevas observaciones (opcional): ")
                nuevo_pedido.modificar_item(id_producto, cantidad, observaciones)
            elif opcion == "4":
                if not nuevo_pedido.items:
                    print("Selecciona algún pedido.")
                    continue
                else:
                    break
            else:
                print("Opción no válida.")

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
            return "no hay pedidos todavia"

        print("\nPedidos en curso:")
        for pedido in self.pedidos:
            if pedido.estado == "En curso":
                print(f"{pedido.id}: {pedido.cliente} ({pedido.mesa})")

        print("\nPedidos listos:")
        for pedido in self.pedidos:
            if pedido.estado == "Listo":
                print(f"{pedido.id}: {pedido.cliente} ({pedido.mesa})")
