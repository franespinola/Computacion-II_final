import socket
from colorama import Fore, Style
import configparser

config = configparser.RawConfigParser()
config.read('configCliente.ini')

if 'CLIENTE' not in config or 'port' not in config['CLIENTE']:
    print(f"{Fore.RED}Falta la configuración en configCliente.ini (sección CLIENTE: port obligatorio).{Style.RESET_ALL}")
    exit(1)

PORT = config['CLIENTE'].getint('port')

ipv4_host = config['CLIENTE'].get('ipv4', '').strip()
if ipv4_host == "":      #si no hago esto me toma la direccion ipv4 disponible en cualquier interfaz de red
    ipv4_host = None

ipv6_host = config['CLIENTE'].get('ipv6', '').strip()
if ipv6_host == "":
    ipv6_host = None

if not ipv4_host and not ipv6_host:
    print(f"{Fore.RED}Debe haber al menos una dirección IP (ipv4 o ipv6) en el archivo de configuración.{Style.RESET_ALL}")
    exit(1)

addrinfos = []

if ipv4_host:
    try:
        ipv4_info = socket.getaddrinfo(ipv4_host, PORT, socket.AF_INET, socket.SOCK_STREAM)
        addrinfos += ipv4_info
    except Exception as e:
        print(f"{Fore.RED}Error al obtener información IPv4 para '{ipv4_host}': {e}{Style.RESET_ALL}")

if ipv6_host:
    try:
        ipv6_info = socket.getaddrinfo(ipv6_host, PORT, socket.AF_INET6, socket.SOCK_STREAM)
        addrinfos += ipv6_info
    except Exception as e:
        print(f"{Fore.RED}Error al obtener información IPv6 para '{ipv6_host}': {e}{Style.RESET_ALL}")

if not addrinfos:
    print(f"{Fore.RED}No se pudo obtener ninguna dirección válida para conectarse.{Style.RESET_ALL}")
    exit(1)

s = None

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
    exit(1)

# Función para solicitar IDs de manera segura (valida que sea entero)
def solicitar_id(mensaje): 
    while True:
        entrada = input(f"{Fore.YELLOW}{mensaje}:{Style.RESET_ALL} ").strip()
        if entrada.isdigit():
            return int(entrada)
        else:
            print(f"{Fore.RED}Entrada inválida. Ingrese un número entero.{Style.RESET_ALL}")

def solicitar_nombre(mensaje):
    """
    Solicita el nombre y no permite que incluya dígitos.
    """
    while True:
        nombre = input(f"{Fore.YELLOW}{mensaje}:{Style.RESET_ALL} ").strip()
        if any(ch.isdigit() for ch in nombre):
            print(f"{Fore.RED}El nombre no puede contener números. Intente nuevamente.{Style.RESET_ALL}")
        else:
            return nombre

try:
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
        try:
            s.sendall(opcion.encode())
        except (ConnectionResetError, BrokenPipeError):
            print(f"{Fore.RED}Error: No se puede enviar datos, la conexión se ha cerrado inesperadamente.{Style.RESET_ALL}")
            break
        except OSError as e:
            print(f"{Fore.RED}Error de envío de datos: {e}{Style.RESET_ALL}")
            break
        try:
            respuesta = s.recv(4096).decode()
            if not respuesta: 
                print(f"{Fore.RED}El servidor cerró la conexión.{Style.RESET_ALL}")
                break
            print(respuesta)
        except (ConnectionResetError, BrokenPipeError):
            print(f"{Fore.RED}Error: El servidor cerró la conexión al recibir datos.{Style.RESET_ALL}")
            break
        except OSError as e:
            print(f"{Fore.RED}Error de recepción de datos: {e}{Style.RESET_ALL}")
            break
        if opcion == "2":
            try:
                nombre = solicitar_nombre("Ingrese su nombre")
                s.sendall(nombre.encode())

                producto = solicitar_id("Ingrese el producto para agregar al pedido (ID)")
                s.sendall(str(producto).encode())

                cantidad = solicitar_id("Ingrese la cantidad")
                s.sendall(str(cantidad).encode())

                observaciones = input(f"{Fore.YELLOW}Ingrese las observaciones:{Style.RESET_ALL} ").strip()
                s.sendall(observaciones.encode())

                respuesta = s.recv(4096).decode()
                print(respuesta)
            except (ConnectionResetError, BrokenPipeError):
                print(f"{Fore.RED}Error: Conexión cerrada mientras se enviaban datos del pedido.{Style.RESET_ALL}")
                break
            except OSError as e:
                print(f"{Fore.RED}Error de envío/recepción en la opción 2: {e}{Style.RESET_ALL}")
                break

        elif opcion == "3":

            if respuesta == "No hay pedidos.":
                continue
            try:
                pregunta = input(f"{Fore.YELLOW}¿Desea agregar otro producto al pedido? (s/n):{Style.RESET_ALL} ").strip().lower()
                s.sendall(pregunta.encode())

                if pregunta == 's':
                    nombre = solicitar_nombre("Ingrese su nombre")
                    s.sendall(nombre.encode())

                    producto = solicitar_id("Ingrese el producto para agregar al pedido (ID)")
                    s.sendall(str(producto).encode())

                    cantidad = solicitar_id("Ingrese la cantidad")
                    s.sendall(str(cantidad).encode())

                    observaciones = input(f"{Fore.YELLOW}Ingrese las observaciones:{Style.RESET_ALL} ").strip()
                    s.sendall(observaciones.encode())

                    respuesta = s.recv(4096).decode()
                    print(respuesta)
            except (ConnectionResetError, BrokenPipeError):
                print(f"{Fore.RED}Error: Conexión cerrada mientras se enviaban/recibían datos adicionales.{Style.RESET_ALL}")
                break
            except OSError as e:
                print(f"{Fore.RED}Error de envío/recepción en la opción 3: {e}{Style.RESET_ALL}")
                break

        elif opcion == "4":
            if respuesta == "No hay pedidos.":
                continue
            try:
                id_pedido = solicitar_id("Ingrese el ID del pedido a modificar")
                s.sendall(str(id_pedido).encode())

                respuesta = s.recv(4096).decode()
                if not respuesta:
                    print(f"{Fore.RED}El servidor cerró la conexión.{Style.RESET_ALL}")
                    break

                if respuesta == "El pedido con el ID proporcionado no existe.":
                    print(respuesta)
                else:
                    producto = solicitar_id("Ingrese el nuevo producto (ID)")
                    s.sendall(str(producto).encode())

                    cantidad = solicitar_id("Ingrese la nueva cantidad")
                    s.sendall(str(cantidad).encode())

                    observaciones = input(f"{Fore.YELLOW}Ingrese las nuevas observaciones:{Style.RESET_ALL} ").strip()
                    s.sendall(observaciones.encode())

                    respuesta = s.recv(4096).decode()
                    print(respuesta)
            except (ConnectionResetError, BrokenPipeError):
                print(f"{Fore.RED}Error: Conexión cerrada mientras se modificaba el pedido.{Style.RESET_ALL}")
                break
            except OSError as e:
                print(f"{Fore.RED}Error de envío/recepción en la opción 4: {e}{Style.RESET_ALL}")
                break

        elif opcion == "5":
            if respuesta == "No hay pedidos.":
                continue

            try:
                id_pedido = solicitar_id("Ingrese el ID del pedido a eliminar")
                s.sendall(str(id_pedido).encode())
                respuesta = s.recv(4096).decode()
                if not respuesta:
                    print(f"{Fore.RED}El servidor cerró la conexión.{Style.RESET_ALL}")
                    break
                print(respuesta)
            except (ConnectionResetError, BrokenPipeError):
                print(f"{Fore.RED}Error: Conexión cerrada mientras se eliminaba el pedido.{Style.RESET_ALL}")
                break
            except OSError as e:
                print(f"{Fore.RED}Error de envío/recepción en la opción 5: {e}{Style.RESET_ALL}")
                break

        elif opcion == "6":
            if respuesta == "No hay pedidos.":
                continue

            try:
                pregunta = input(f"{Fore.YELLOW}¿Desea enviar el pedido? (s/n):{Style.RESET_ALL} ").strip().lower()
                s.sendall(pregunta.encode())

                if pregunta == 's':
                    respuesta = s.recv(4096).decode()
                    if not respuesta:
                        print(f"{Fore.RED}El servidor cerró la conexión.{Style.RESET_ALL}")
                        break
                    print(respuesta)

                    respuesta = s.recv(4096).decode()
                    if not respuesta:
                        print(f"{Fore.RED}El servidor cerró la conexión.{Style.RESET_ALL}")
                        break
                    print(respuesta)

                    break
            except (ConnectionResetError, BrokenPipeError):
                print(f"{Fore.RED}Error: Conexión cerrada mientras se enviaba el pedido.{Style.RESET_ALL}")
                break
            except OSError as e:
                print(f"{Fore.RED}Error de envío/recepción en la opción 6: {e}{Style.RESET_ALL}")
                break

except KeyboardInterrupt:
    print(f"\n{Fore.RED}Cliente cerrado por el usuario.{Style.RESET_ALL}")
finally:
    if s:
        s.close()
    print(f"{Fore.RED}Conexión cerrada.{Style.RESET_ALL}")
