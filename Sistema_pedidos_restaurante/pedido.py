import time
from producto import PedidoItem

class Pedido:
    def __init__(self, id, cliente, mesa):
        self.id = id
        self.cliente = cliente
        self.mesa = mesa
        self.estado = "En curso"
        self.items = []
        self.total = 0

    def agregar_item(self, producto, cantidad, observaciones):
        nuevo_item = PedidoItem(producto, cantidad, observaciones)
        self.items.append(nuevo_item)
        self.calcular_total()

    def modificar_item(self, id_item, cantidad, observaciones):
        for item in self.items:
            if item.producto.id == id_item:
                item.cantidad = cantidad
                item.observaciones = observaciones
                self.calcular_total()
                break

    def eliminar_item(self, id_item):
        for i, item in enumerate(self.items):
            if item.producto.id == id_item:
                del self.items[i]
                self.calcular_total()
                break

    def calcular_total(self):
        self.total = sum(item.calcular_subtotal() for item in self.items)

    def enviar_a_cocina(self):
        print(f"Pedido #{self.id} enviado a cocina.")
        time.sleep(2)
        self.cocina.procesar_pedido(self)

    def notificar_cliente_pedido_listo(self):
        print(f"Pedido #{self.id} listo para ser retirado.")

    def __str__(self):
        pedido_str = f"""
        Pedido: {self.id}
        Cliente: {self.cliente}
        Mesa: {self.mesa}
        Estado: {self.estado}
        """
        pedido_str += "\n".join(str(item) for item in self.items)
        pedido_str += f"\nTotal: ${self.total:.2f}"
        return pedido_str
