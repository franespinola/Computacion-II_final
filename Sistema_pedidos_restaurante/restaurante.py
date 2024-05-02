from pedido import Pedido
class Restaurante:
    def __init__(self, carta):
        self.carta = carta
        self.pedidos = []

    def tomar_pedido(self, nombre, producto, cantidad, observaciones):
        pedido = Pedido(nombre, producto, cantidad, observaciones)
        self.pedidos.append(pedido)
    
    def mostrar_pedidos(self):
        respuesta = ""
        for pedido in self.pedidos:
            respuesta += str(pedido) + "\n"
        return respuesta

    def modificar_pedido(self, id_pedido, producto, cantidad, observaciones):
        for pedido in self.pedidos:
            if pedido.id == id_pedido:
                pedido.modificar_item(producto, cantidad, observaciones)
                break

    def eliminar_pedido(self, id_pedido):
        self.pedidos = [pedido for pedido in self.pedidos if pedido.id != id_pedido]
