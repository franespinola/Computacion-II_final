# producto.py

class Producto:
    def __init__(self, id, nombre, precio, categoria, descripcion):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.descripcion = descripcion

    def __str__(self):
        return f"""
        Producto: {self.nombre}
        ID: {self.id}
        Precio: ${self.precio:.2f}
        Categoría: {self.categoria}
        Descripción: {self.descripcion}
        """

class PedidoItem:
    def __init__(self, producto, cantidad, observaciones):
        self.producto = producto
        self.cantidad = cantidad
        self.observaciones = observaciones

    def calcular_subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"""
        Item: {self.producto.nombre} ({self.cantidad} unidades)
        Subtotal: ${self.calcular_subtotal():.2f}
        Observaciones: {self.observaciones}
        """
