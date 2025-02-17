import socket
from colorama import Fore, Style

# Direcciones para IPv4 e IPv6
ipv4_host = '169.254.22.147'
ipv6_host = 'fe80::a51f:508b:c5b5:41a%13'
PORT = 50007

s = None  # Inicializar el socket

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
        def solicitar_id(mensaje): 
            while True:
                entrada = input(f"{Fore.YELLOW}{mensaje}:{Style.RESET_ALL} ").strip()
                if entrada.isdigit():
                    return int(entrada)
                else:
                    print(f"{Fore.RED}Entrada inválida. Ingrese un número entero.{Style.RESET_ALL}")
        while True:
            print(f"\n{Fore.CYAN}Opciones:{Style.RESET_ALL}")
            print("1. Mostrar carta")
            print("2. Tomar pedido")
            print("3. Mostrar pedidos")
            print("4. Modificar pedido")
            print("5. Eliminar pedido")
            print("6. Enviar Pedido")

            opcion = input(f"{Fore.GREEN}Ingrese opción:{Style.RESET_ALL} ").strip()
            if opcion not in ["1", "2", "3", "4", "5", "6"]:
                print(f"{Fore.RED}Opción no válida....{Style.RESET_ALL}")
                continue

            s.sendall(opcion.encode())
            respuesta = s.recv(4096).decode()
            print(respuesta)

            if opcion == "2":
                nombre = input(f"{Fore.YELLOW}Ingrese su nombre:{Style.RESET_ALL} ").strip()
                s.sendall(nombre.encode())
                producto = solicitar_id("Ingrese el producto para agregar al pedido (ID)")
                s.sendall(str(producto).encode())
                cantidad = solicitar_id("Ingrese la cantidad")
                s.sendall(str(cantidad).encode())
                observaciones = input(f"{Fore.YELLOW}Ingrese las observaciones:{Style.RESET_ALL} ").strip()
                s.sendall(str(observaciones).encode())
                respuesta = s.recv(4096).decode()
                print(respuesta)

            elif opcion == "3":
                if respuesta == "No hay pedidos.":
                    continue
                pregunta = input(f"{Fore.YELLOW}¿Desea agregar otro producto al pedido? (s/n):{Style.RESET_ALL} ").strip().lower()
                s.sendall(pregunta.encode())
                if pregunta == 's':
                    nombre = input(f"{Fore.YELLOW}Ingrese su nombre:{Style.RESET_ALL} ").strip()
                    s.sendall(nombre.encode())
                    producto = solicitar_id("Ingrese el producto para agregar al pedido (ID)")
                    s.sendall(str(producto).encode())
                    cantidad = solicitar_id("Ingrese la cantidad")
                    s.sendall(str(cantidad).encode())
                    observaciones = input(f"{Fore.YELLOW}Ingrese las observaciones:{Style.RESET_ALL} ").strip()
                    s.sendall(str(observaciones).encode())
                    respuesta = s.recv(4096).decode()
                    print(respuesta)

            elif opcion == "4":
                if respuesta == "No hay pedidos.":
                    continue
                id_pedido = solicitar_id("Ingrese el ID del pedido a modificar")
                s.sendall(str(id_pedido).encode())
                respuesta = s.recv(4096).decode()
                if respuesta == "El pedido con el ID proporcionado no existe.":
                    print(respuesta)
                else:
                    producto = solicitar_id("Ingrese el nuevo producto (ID)")
                    s.sendall(str(producto).encode())
                    cantidad = solicitar_id("Ingrese la nueva cantidad")
                    s.sendall(str(cantidad).encode())
                    observaciones = input(f"{Fore.YELLOW}Ingrese las nuevas observaciones:{Style.RESET_ALL} ").strip()
                    s.sendall(str(observaciones).encode())
                    respuesta = s.recv(4096).decode()
                    print(respuesta)

            elif opcion == "5":
                if respuesta == "No hay pedidos.":
                    continue
                id_pedido = solicitar_id("Ingrese el ID del pedido a eliminar")
                s.sendall(str(id_pedido).encode())
                respuesta = s.recv(4096).decode()
                print(respuesta)

            elif opcion == "6":
                if respuesta == "No hay pedidos.":
                    continue
                pregunta = input(f"{Fore.YELLOW}¿Desea enviar el pedido? (s/n):{Style.RESET_ALL} ").strip().lower()
                s.sendall(pregunta.encode())
                if pregunta == 's':
                    respuesta = s.recv(4096).decode()
                    print(respuesta)
                    respuesta = s.recv(4096).decode()
                    print(respuesta)
                    break

    finally:
        s.close()
        print(f"{Fore.RED}Conexión cerrada.{Style.RESET_ALL}")
