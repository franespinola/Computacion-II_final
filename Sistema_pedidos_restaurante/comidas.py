import json
class Plato:
    def __init__(self, nombre, precio, descripcion):
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion

class Menu:
    def __init__(self):
        self.platos = []

    def agregar_plato(self, plato):
        self.platos.append(plato)

    def obtener_menu(self):
        return self.platos


menu=Menu()
menu.agregar_plato(Plato("Sopa de pollo", 10, "Sopa de pollo con verduras"))
menu.agregar_plato(Plato("Hamburguesa", 15, "Hamburguesa con queso y papas fritas"))
menu.agregar_plato(Plato("Pizza", 20, "Pizza de peperoni"))
menu.agregar_plato(Plato("Ensalada", 5, "Ensalada de lechuga y tomate"))
menu.agregar_plato(Plato("Spaghetti", 12, "Spaghetti con salsa de tomate"))
menu.agregar_plato(Plato("Tacos", 10, "Tacos de carne asada"))
menu.agregar_plato(Plato("Hot dog", 8, "Hot dog con mostaza y catsup"))
menu.agregar_plato(Plato("Pollo asado", 15, "Pollo asado con papas fritas"))



def plato_a_json(plato):
    return json.dumps(plato.__dict__)

def menu_a_json(menu):
    return json.dumps([plato_a_json(plato) for plato in menu.obtener_menu()])