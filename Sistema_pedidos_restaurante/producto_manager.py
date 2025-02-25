from producto import Producto
from menu_manager import Menu

# Cargar el menú desde el archivo 'carta.json'
menu = Menu('carta.json')

while True:
    print("\nOpciones:")
    print("1. Agregar producto")
    print("2. Eliminar producto")
    print("0. Salir")
    opcion = input("Seleccione la opción deseada (1/2/0): ")

    if opcion == '0':
        print("Saliendo del programa...")
        break

    elif opcion == '1':
        # Opción para agregar producto

        # Validación para que el nombre no sea un entero
        while True:
            nombre = input("Ingrese el nombre del producto: ")
            if nombre.strip().isdigit():
                print("El nombre no puede ser un número. Por favor ingrese un nombre válido.")
            else:
                break

        precio_input = input("Ingrese el precio del producto: ")
        try:
            precio = float(precio_input)
        except ValueError:
            print("El precio ingresado no es válido.")
            continue  # Vuelve a mostrar el menú

        categoria = input("Ingrese la categoría del producto: ")
        descripcion = input("Ingrese la descripción del producto: ")

        # Calcular el siguiente id disponible
        if menu.productos:
            nuevo_id = max(prod.id for prod in menu.productos) + 1
        else:
            nuevo_id = 1

        nuevo_producto = Producto(nuevo_id, nombre, precio, categoria, descripcion)
        menu.agregar_producto(nuevo_producto)
        print("Producto agregado exitosamente!")

    elif opcion == '2':
        # Opción para eliminar producto
        if not menu.productos:
            print("No hay productos en la carta para eliminar.")
        else:
            print("Productos actuales:")
            for prod in menu.productos:
                print(f"ID: {prod.id} - {prod.nombre}")
            id_input = input("Ingrese el ID del producto que desea eliminar: ")
            try:
                id_de_eliminacion = int(id_input)
            except ValueError:
                print("El ID ingresado no es válido.")
                continue

            # Verificar si existe el producto con ese ID
            if any(prod.id == id_de_eliminacion for prod in menu.productos):
                menu.eliminar_producto(id_de_eliminacion)
                print("Producto eliminado exitosamente!")
            else:
                print("No se encontró un producto con ese ID.")

    else:
        print("Opción no válida.")
