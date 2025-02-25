import json
from producto import Producto

class Menu:
    def __init__(self, carta_json):
        self.carta_json = carta_json
        self.productos = []   #voy a tener una lista de objetos producto
        self.load()

    def load(self):
        try:
            with open(self.carta_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.productos = [Producto(**prod) for prod in data["productos"]] # Convierto cada diccionario a un objeto Producto
        except FileNotFoundError:
            print("No se encontró el archivo de carta. Se inicializa con lista vacía.")
            self.productos = []
        except Exception as e:
            print("Error al cargar la carta:", e)
            self.productos = []

    def guardar(self):
        data = {"productos": [self._producto_to_dict(prod) for prod in self.productos]}
        with open(self.carta_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _producto_to_dict(self, producto): #funcion para convertir un objeto producto a diccionario
        return {
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "categoria": producto.categoria,
            "descripcion": producto.descripcion
        }

    def agregar_producto(self, producto):
        self.productos.append(producto)
        self.guardar()

    def eliminar_producto(self, producto_id):
        self.productos = [prod for prod in self.productos if prod.id != producto_id] #lista por comprension donde recorro dentro de la lista de self.productos y dejo solo los productos que sean diferentes a la id que paso en producto_id
        self.guardar()
