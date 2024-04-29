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
        print("4. Salir")

        opcion = input("Ingrese opción: ")
        s.sendall(opcion.encode())

        data = s.recv(1024)

        respuesta = data.decode()
        print(repr(respuesta))
        if respuesta == "Saliendo del programa.":
            break
finally:
    s.close()
    print("Conexión cerrada.")