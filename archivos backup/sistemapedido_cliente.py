elif opcion == "3":
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