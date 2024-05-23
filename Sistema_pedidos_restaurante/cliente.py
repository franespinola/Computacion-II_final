import socket

HOST = 'localhost'
PORT = 50007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

try:
    while True:
        print("\nOpciones:")
        print("1. Mostrar carta")
        print("2. Tomar pedido")
        print("3. Mostrar pedidos")
        print("4. Modificar pedido")
        print("5. Eliminar pedido")
        print("6. Enviar Pedido")

        opcion = input("Ingrese opción: ")
        if opcion not in ["1", "2", "3", "4", "5", "6"]:
            print("Opción no válida....")
        else:    
            s.sendall(opcion.encode())
            respuesta = s.recv(1024).decode()
            print(respuesta)

        if opcion == "2":
            nombre = input("Ingrese su nombre: ")
            s.sendall(nombre.encode())
            producto = int(input("Ingrese el producto para agregar al pedido(ID): "))
            s.sendall(str(producto).encode())
            cantidad = int(input("Ingrese la cantidad: "))
            s.sendall(str(cantidad).encode())
            observaciones = input("Ingrese las observaciones: ")
            s.sendall(str(observaciones).encode())
            respuesta = s.recv(1024).decode()
            print(respuesta)
            
        elif opcion == "3":
            if respuesta == "No hay pedidos.":  # Si no hay pedidos, no se puede agregar otro producto
                continue
            else:
                pregunta = input("¿Desea agregar otro producto al pedido? (s/n)")
                s.sendall(pregunta.encode())
                if pregunta.lower() == 's':
                    producto = int(input("Ingrese el producto para agregar al pedido(ID): "))
                    s.sendall(str(producto).encode())
                    cantidad = int(input("Ingrese la cantidad: "))
                    s.sendall(str(cantidad).encode())
                    observaciones = input("Ingrese las observaciones: ")
                    s.sendall(str(observaciones).encode())
                    respuesta=s.recv(1024).decode()
                    print(respuesta)

        elif opcion == "4":
            id_pedido = int(input("Ingrese el ID del pedido a modificar: "))
            s.sendall(str(id_pedido).encode())
            respuesta = s.recv(1024).decode()
            if respuesta == "El pedido con el ID proporcionado no existe.":
                print(respuesta)
            else:
                producto = int(input("Ingrese el nuevo producto (ID): "))
                s.sendall(str(producto).encode())
                cantidad = int(input("Ingrese la nueva cantidad: "))
                s.sendall(str(cantidad).encode())
                observaciones = input("Ingrese las nuevas observaciones: ")
                s.sendall(str(observaciones).encode())
                respuesta=s.recv(1024).decode()
                print(respuesta)

        elif opcion == "5":
            id_pedido = int(input("Ingrese el ID del pedido a eliminar: "))
            s.sendall(str(id_pedido).encode())
            respuesta = s.recv(1024).decode()
            print(respuesta)

        elif opcion == "6":
            if respuesta == "No hay pedidos.":
                continue
            else:
                pregunta = input("¿Desea enviar el pedido? (s/n)")
                s.sendall(pregunta.encode())
                if pregunta.lower() == 's':
                    respuesta = s.recv(1024).decode()
                    print(respuesta)
                    respuesta = s.recv(1024).decode()
                    print(respuesta)
                    break
                     
finally:
    s.close()
    print("Conexión cerrada.")