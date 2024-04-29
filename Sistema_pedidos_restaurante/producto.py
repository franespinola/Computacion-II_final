class Producto:
    def __init__(self, id, nombre, precio, categoria, descripcion):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.descripcion = descripcion

    def __str__(self):
        return f"{self.nombre} ({self.categoria}): {self.descripcion} - ${self.precio:.2f}"
