from datetime import datetime
class Pedido:
    id = 1
    #traigo el objeto producto
    def __init__(self, nombre, producto, cantidad, observaciones):
        self.id = Pedido.id
        self.nombre = nombre
        self.producto = producto
        self.cantidad = cantidad
        self.observaciones = observaciones
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Fecha y hora exacta
        Pedido.id += 1  #por cada instancia q se crea se incrementa el id

    def __str__(self):
        return f"""
        Pedido: {self.id}
        Nombre: {self.nombre}
        Producto: {self.producto.nombre}
        Precio: {self.producto.precio}$
        Cantidad: {self.cantidad}
        Observaciones: {self.observaciones}
        Fecha y Hora: {self.timestamp}
        -------------------------
        Subtotal: {self.calcular_subtotal():.2f}$ 
        """

    def calcular_subtotal(self):
        return self.producto.precio * self.cantidad