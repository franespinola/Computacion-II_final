import socket
from colorama import Fore, Style

# Define las direcciones para IPv4 e IPv6
ipv4_host = '192.168.1.42'
ipv6_host = 'fda8:4ac5:c10a:1a8f:f299:931d:e6be:9dd5'
PORT = 50007

s = None  # Inicializar la variable del socket

# Obtener la información de la dirección para ambos tipos de direcciones
ipv4_info = socket.getaddrinfo(ipv4_host, PORT, socket.AF_INET, socket.SOCK_STREAM)
ipv6_info = socket.getaddrinfo(ipv6_host, PORT, socket.AF_INET6, socket.SOCK_STREAM)

# Concatenar la información de ambas listas para iterar sobre ellas
addrinfos = ipv4_info + ipv6_info

for res in addrinfos:
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
        s.connect(sa)
        if af == socket.AF_INET6:
            print(f"{Fore.GREEN}Conexión establecida por IPv6 a {sa[0]}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}Conexión establecida por IPv4 a {sa}{Style.RESET_ALL}")
        break
    except OSError as msg:
        print(f"{Fore.RED}Error al conectar con {sa}: {msg}{Style.RESET_ALL}")
        s = None

if s is None:
    print(f"{Fore.RED}No se pudo conectar al servidor{Style.RESET_ALL}")
else:
    try:
        while True:
            print(f"\n{Fore.CYAN}Opciones:{Style.RESET_ALL}")
            print("1. Mostrar carta")
            print("2. Tomar pedido")
            print("3. Mostrar pedidos")
            print("4. Modificar pedido")
            print("5. Eliminar pedido")
            print("6. Enviar Pedido")

            opcion = input(f"{Fore.GREEN}Ingrese opción:{Style.RESET_ALL} ")
            if opcion not in ["1", "2", "3", "4", "5", "6"]:
                print(f"{Fore.RED}Opción no válida....{Style.RESET_ALL}")
                continue
            
            s.sendall(opcion.encode())
            respuesta = s.recv(4096).decode()  # Aumentar el tamaño del búfer de recepción
            print(respuesta)

            if opcion == "2":
                nombre = input(f"{Fore.YELLOW}Ingrese su nombre:{Style.RESET_ALL} ")
                s.sendall(nombre.encode())
                producto = int(input(f"{Fore.YELLOW}Ingrese el producto para agregar al pedido (ID):{Style.RESET_ALL} "))
                s.sendall(str(producto).encode())
                cantidad = int(input(f"{Fore.YELLOW}Ingrese la cantidad:{Style.RESET_ALL} "))
                s.sendall(str(cantidad).encode())
                observaciones = input(f"{Fore.YELLOW}Ingrese las observaciones:{Style.RESET_ALL} ")
                s.sendall(str(observaciones).encode())
                respuesta = s.recv(4096).decode()
                print(respuesta)
                
            elif opcion == "3":
                if respuesta == "No hay pedidos.":
                    continue
                pregunta = input(f"{Fore.YELLOW}¿Desea agregar otro producto al pedido? (s/n):{Style.RESET_ALL} ")
                s.sendall(pregunta.encode())
                if pregunta.lower() == 's':
                    nombre = input(f"{Fore.YELLOW}Ingrese su nombre:{Style.RESET_ALL} ")
                    s.sendall(nombre.encode())
                    producto = int(input(f"{Fore.YELLOW}Ingrese el producto para agregar al pedido (ID):{Style.RESET_ALL} "))
                    s.sendall(str(producto).encode())
                    cantidad = int(input(f"{Fore.YELLOW}Ingrese la cantidad:{Style.RESET_ALL} "))
                    s.sendall(str(cantidad).encode())
                    observaciones = input(f"{Fore.YELLOW}Ingrese las observaciones:{Style.RESET_ALL} ")
                    s.sendall(str(observaciones).encode())
                    respuesta = s.recv(4096).decode()
                    print(respuesta)

            elif opcion == "4":
                if respuesta == "No hay pedidos.":
                    continue
                id_pedido = int(input(f"{Fore.YELLOW}Ingrese el ID del pedido a modificar:{Style.RESET_ALL} "))
                s.sendall(str(id_pedido).encode())
                respuesta = s.recv(4096).decode()
                if respuesta == "El pedido con el ID proporcionado no existe.":
                    print(respuesta)
                else:
                    producto = int(input(f"{Fore.YELLOW}Ingrese el nuevo producto (ID):{Style.RESET_ALL} "))
                    s.sendall(str(producto).encode())
                    cantidad = int(input(f"{Fore.YELLOW}Ingrese la nueva cantidad:{Style.RESET_ALL} "))
                    s.sendall(str(cantidad).encode())
                    observaciones = input(f"{Fore.YELLOW}Ingrese las nuevas observaciones:{Style.RESET_ALL} ")
                    s.sendall(str(observaciones).encode())
                    respuesta = s.recv(4096).decode()
                    print(respuesta)

            elif opcion == "5":
                if respuesta == "No hay pedidos.":
                    continue
                id_pedido = int(input(f"{Fore.YELLOW}Ingrese el ID del pedido a eliminar:{Style.RESET_ALL} "))
                s.sendall(str(id_pedido).encode())
                respuesta = s.recv(4096).decode()
                print(respuesta)

            elif opcion == "6":
                if respuesta == "No hay pedidos.":
                    continue
                pregunta = input(f"{Fore.YELLOW}¿Desea enviar el pedido? (s/n):{Style.RESET_ALL} ")
                s.sendall(pregunta.encode())
                if pregunta.lower() == 's':
                    respuesta = s.recv(4096).decode()
                    print(respuesta)
                    respuesta = s.recv(4096).decode()  # Esperar el mensaje del servidor indicando que el pedido está listo
                    print(respuesta)
                    break
                         
    finally:
        s.close()
        print(f"{Fore.RED}Conexión cerrada.{Style.RESET_ALL}")
