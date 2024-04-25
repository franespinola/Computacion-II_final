import time

class Cocina:
    def __init__(self):
        self.pedidos = []
        self.pedidos_listos = []

    def procesar_pedido(self, pedido):
        pedido.estado = "En preparación"
        self.pedidos.append(pedido)
        time.sleep(5)
        self.notificar_pedido_listo(pedido)

    def notificar_pedido_listo(self, pedido):
        pedido.estado = "Listo"
        self.pedidos.remove(pedido)
        self.pedidos_listos.append(pedido)
        pedido.restaurante.notificar_cliente_pedido_listo(pedido)
