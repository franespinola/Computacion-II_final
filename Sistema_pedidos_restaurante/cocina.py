import socket

HOST = 'localhost'
PORT = 50007
print("Conectando al servidor...")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    s.connect(server_address)

     # Enviar datos al servidor
    message = "¡Conexión exitosa desde la cocina!"
    s.sendall(message.encode())

    # Esperar la respuesta del servidor
    data = s.recv(1024)
    print("Respuesta del servidor:", data.decode())

except Exception as e:
    print("Error al conectar al servidor:", str(e))

finally:
    # Cerrar la conexión
    s.close()

