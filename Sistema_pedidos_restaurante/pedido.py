class Pedido:
    id = 0

    def __init__(self, nombre, producto, cantidad, observaciones):
        self.id = Pedido.id
        self.nombre = nombre
        self.producto = producto
        self.cantidad = cantidad
        self.observaciones = observaciones
        Pedido.id += 1  #por cada instancia q se crea se incrementa el id

    def __str__(self):
        return f"""
        Pedido: {self.id}
        Nombre: {self.nombre}
        Producto: {self.producto}
        Cantidad: {self.cantidad}
        Observaciones: {self.observaciones}
        """

