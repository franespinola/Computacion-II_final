class Pedido:
    id = 0

    def __init__(self, nombre, producto, cantidad, observaciones):
        self.id = Pedido.id
        self.nombre = nombre
        self.producto = producto
        self.cantidad = cantidad
        self.observaciones = observaciones
        Pedido.id += 1

    def __str__(self):
        return f"""
        Pedido: {self.id}
        Nombre: {self.nombre}
        Producto: {self.producto}
        Cantidad: {self.cantidad}
        Observaciones: {self.observaciones}
        """

    def modificar_item(self, producto, cantidad, observaciones):
        self.producto = producto
        self.cantidad = cantidad
        self.observaciones = observaciones

    def eliminar_item(self):
        self.producto = None
        self.cantidad = None
        self.observaciones = None
