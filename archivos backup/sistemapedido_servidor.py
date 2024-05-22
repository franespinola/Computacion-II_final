elif opcion == "3":
            client_socket.sendall(restaurante.mostrar_pedidos().encode())
            if restaurante.mostrar_pedidos() == "No hay pedidos.":
                continue
            pregunta = client_socket.recv(1024).decode()
            if pregunta.lower() == 's':
                producto_id = int(client_socket.recv(1024).decode())
                cantidad = int(client_socket.recv(1024).decode())
                observaciones = client_socket.recv(1024).decode()
                producto = next((prod for prod in carta if prod.id == producto_id), None)
                if producto is not None:
                    restaurante.tomar_pedido(nombre, producto, cantidad, observaciones)  # Tomar un pedido usando el método de Restaurante
                else:
                    client_socket.sendall("Error: Producto no encontrado en la carta.".encode())
                client_socket.sendall(restaurante.mostrar_pedidos().encode())