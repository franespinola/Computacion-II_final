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
        s.sendall(opcion.encode()) #convierto en bytes la cadena de texto para que pueda ser enviada a traves del socket con s.sendall
        respuesta = s.recv(1024).decode() #decodificamos la respuesta del servidor para que pueda ser leida como una cadena de texto
        print (respuesta) #recibo la respuesta del servidor y la imprimo en pantalla
        
        if opcion == "2":
            nombre = input("Ingrese su nombre: ")
            s.sendall(nombre.encode())
            producto = int(input("Ingrese el producto para agregar al pedido(ID): "))
            s.sendall(str(producto).encode())
            cantidad = int(input("Ingrese la cantidad: "))
            s.sendall(str(cantidad).encode())
            observaciones = input("Ingrese las observaciones: ")
            s.sendall(observaciones.encode())
        if opcion == "4":
            break
finally:
    s.close()
    print("Conexión cerrada.")