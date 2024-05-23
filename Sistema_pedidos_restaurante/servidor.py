import socket
import threading
from carta import carta
from restaurante import Restaurante
from collections import defaultdict
from colorama import Fore, Style
import logging

# Configuracion del logging
logging.basicConfig(filename='servidor.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s') 

def handle_client(client_socket):
    restaurante = Restaurante(carta) 
    while True:
        opcion = client_socket.recv(1024).decode()  #hago la decodificacion de los datos con decode. Recordando que vienen en bytes
        print("Opción recibida:", opcion)

    #-------------Mostrar carta---------------------------------------- #   
        if opcion == "1":
            productos_por_categoria = defaultdict(list) # Agrupar los productos por categoría
            respuesta = "" # Crear la respuesta
            for producto in carta:
                productos_por_categoria[producto.categoria].append(producto)
            for categoria in productos_por_categoria:
                respuesta += f"\n\n{Fore.GREEN}{categoria}{Style.RESET_ALL}:\n\n" # Agregar el título de la categoría
                respuesta += "\n".join(str(producto) for producto in productos_por_categoria[categoria]) # Agregar los productos de la categoría
            client_socket.sendall(respuesta.encode())
            logging.info(f"Cliente {client_socket.getpeername()} - Carta mostrada.") 

    #-------------Tomar pedido---------------------------------------- # 
        elif opcion == "2":
            respuesta = f"{Fore.GREEN}Tomando pedido...{Style.RESET_ALL}"
            client_socket.sendall(respuesta.encode())
            nombre = client_socket.recv(1024).decode() # Recibir el nombre del cliente
            producto_id = int(client_socket.recv(1024).decode()) # Recibir el ID del producto
            cantidad = int(client_socket.recv(1024).decode()) # Recibir la cantidad
            observaciones = client_socket.recv(1024).decode() # Recibir las observaciones
            # Buscar el objeto Producto correspondiente al ID recibido
            producto = next((prod for prod in carta if prod.id == producto_id), None) #busca en la lista carta el primer objeto Producto cuyo id coincida con el valor de producto_id. Si lo encuentra, asigna ese objeto Producto a la variable producto. Si no lo encuentra, asigna None a producto.
            if producto is not None:# Verificar si se encontró el producto
                restaurante.tomar_pedido(nombre, producto, cantidad, observaciones)# Tomar un pedido usando el método de Restaurante
                client_socket.sendall("Pedido tomado con éxito.".encode())
                logging.info(f"Cliente {client_socket.getpeername()} - Pedido tomado: {restaurante.pedidos[-1]}")  # Imprime el último pedido añadido
            else:
                logging.error(f"Cliente {client_socket.getpeername()} - Error: Producto no encontrado en la carta.")
                client_socket.sendall("Error: Producto no encontrado en la carta.".encode())# Enviar un mensaje de error si el producto no se encuentra en la carta
            
    #-------------Mostrar pedido---------------------------------------- #     
        elif opcion == "3":
            client_socket.sendall(restaurante.mostrar_pedidos().encode())
            if restaurante.mostrar_pedidos() == "No hay pedidos.":
                logging.info(f"Cliente {client_socket.getpeername()} - No hay pedidos.")
                continue
            else:
                logging.info(f"Cliente {client_socket.getpeername()} - Pedidos mostrados")
            pregunta = client_socket.recv(1024).decode()
            if pregunta.lower() == 's':
                producto_id = int(client_socket.recv(1024).decode())
                cantidad = int(client_socket.recv(1024).decode())
                observaciones = client_socket.recv(1024).decode()
                producto = next((prod for prod in carta if prod.id == producto_id), None)
                if producto is not None:
                    restaurante.tomar_pedido(nombre, producto, cantidad, observaciones)  # Tomar un pedido usando el método de Restaurante
                else:
                    logging.error(f"Cliente {client_socket.getpeername()} - Error: Producto no encontrado en la carta.")
                    client_socket.sendall("Error: Producto no encontrado en la carta.".encode())
                client_socket.sendall(restaurante.mostrar_pedidos().encode())
  
    #-------------Modificar pedido---------------------------------------- #  
        elif opcion == "4":
            mensaje = f"{Fore.YELLOW}Modificando pedido...{Style.RESET_ALL}"
            client_socket.sendall(mensaje.encode())
            id_pedido = int(client_socket.recv(1024).decode())
            if not restaurante.pedido_existe(id_pedido):
                client_socket.sendall("El pedido con el ID proporcionado no existe.".encode())
                logging.error(f"Cliente {client_socket.getpeername()} - Error: Pedido no encontrado para su modificacion.")
            else:
                logging.info(f"Cliente {client_socket.getpeername()} - Pedido modificado: {id_pedido}")
                client_socket.sendall("Pedido modificado con éxito.".encode())
                # Recibir el nuevo producto, cantidad y observaciones del cliente
                producto_id = int(client_socket.recv(1024).decode())
                cantidad = int(client_socket.recv(1024).decode())
                observaciones = client_socket.recv(1024).decode()
                # Buscar el objeto Producto correspondiente al producto_id
                producto = next((prod for prod in carta if prod.id == producto_id), None)
                if producto is not None:
                    # Si se encuentra el producto, modificar el pedido
                    client_socket.sendall(restaurante.modificar_pedido(id_pedido, producto, cantidad, observaciones).encode())
                else:
                    # Si no se encuentra el producto, enviar un mensaje de error al cliente
                    logging.error(f"Cliente {client_socket.getpeername()} - Error: Producto no encontrado en la carta.")
                    client_socket.sendall("Error: Producto no encontrado en la carta.".encode())

        #-------------Eliminar pedido---------------------------------------- # 
        elif opcion == "5":
            mensaje = f"{Fore.RED}Eliminando pedido.....{Style.RESET_ALL}"
            client_socket.sendall(mensaje.encode())
            id_pedido = client_socket.recv(1024).decode()
            if not restaurante.pedido_existe(id_pedido):
                logging.error(f"Cliente {client_socket.getpeername()} - Error: Pedido no encontrado para su eliminacion.")
                client_socket.sendall("El pedido con el ID proporcionado no existe.".encode())
            else:
                logging.info(f"Cliente {client_socket.getpeername()} - Pedido eliminado: {id_pedido}")
                restaurante.eliminar_pedido(id_pedido)
                client_socket.sendall("Pedido eliminado con éxito.".encode())
                print(f"Cliente {client_socket.getpeername()} - Pedido eliminado: {id_pedido}")
        
        #-------------Enviar pedido a cocina y salir(resetear pedidos)--------------------------------------- # 
        elif opcion == "6":
            client_socket.sendall(restaurante.mostrar_pedidos().encode())
            if restaurante.mostrar_pedidos() == "No hay pedidos.":
                continue
            pregunta = client_socket.recv(1024).decode()
            if pregunta.lower() == 's':
                logging.info(f"Cliente {client_socket.getpeername()} - Pedido enviado a cocina")
                client_socket.sendall("Pedido enviado a cocina. Espere a ser llamado.".encode())    
                print(f"Cliente {client_socket.getpeername()} - Pedido enviado a cocina: {restaurante.mostrar_pedidos()}")  

def server():
    HOST = 'localhost'
    PORT = 50007
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()
server()






    


