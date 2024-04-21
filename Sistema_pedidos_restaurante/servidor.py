# Echo server program
import socket
import sys
import threading
import comidas

def handle_client(client_socket):
    # Handle the client connection: receive data, then send it back
    menu_json = comidas.menu_a_json(comidas.menu)
    client_socket.send(menu_json.encode())

    # Recibir la selección del cliente
    seleccion = client_socket.recv(1024).decode()
    print(f"Cliente seleccionó: {seleccion}")

    # Manejar la selección del cliente
    comidas.manejar_seleccion(client_socket, seleccion)

    client_socket.close()

def server_loop():
    HOST = 'localhost'              # Symbolic name meaning all available interfaces
    PORT = 50007              # Arbitrary non-privileged port
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                                  socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            s = None
            continue
        try:
            s.bind(sa)
            s.listen(5)
        except OSError as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print('could not open socket')
        sys.exit(1)

    while True:  # Agregamos un bucle externo para seguir aceptando nuevas conexiones
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()

server_thread = threading.Thread(target=server_loop, daemon=True)

# Start the server thread
server_thread.start()

try:
    # Wait for keyboard interrupt
    while True: pass
except KeyboardInterrupt:
    print("Server shutting down.")
    sys.exit(0)
    


