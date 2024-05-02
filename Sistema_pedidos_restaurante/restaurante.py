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
        id_pedido = int(id_pedido) #convierto la id del pedido a entero ya que del servidor viene en formato str
        for pedido in self.pedidos:
            if pedido.id == id_pedido:
                pedido.producto = producto
                pedido.cantidad = cantidad
                pedido.observaciones = observaciones
        return self.mostrar_pedidos()

    def eliminar_pedido(self, id_pedido):
        id_pedido = int(id_pedido)
        self.pedidos = [pedido for pedido in self.pedidos if pedido.id != id_pedido] #creo una lista con todos los pedidos menos el que quiero eliminar
        return self.mostrar_pedidos()
