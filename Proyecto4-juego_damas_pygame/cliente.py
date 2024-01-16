import socket
import pickle
import threading

class ClienteDamas:
    def __init__(self, nombre, host, port):
        self.nombre = nombre
        self.host = host
        self.port = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conectar_al_servidor()

    def conectar_al_servidor(self):
        self.socket_cliente.connect((self.host, self.port))
        self.socket_cliente.send(pickle.dumps(self.nombre))
        bienvenida = pickle.loads(self.socket_cliente.recv(1024))
        print(bienvenida)

    def recibir_estado(self):
        while True:
            estado = pickle.loads(self.socket_cliente.recv(1024))
            print(f"Estado actualizado: {estado}")

    def enviar_movimiento(self, movimiento):
        self.socket_cliente.send(pickle.dumps(movimiento))

if __name__ == "__main__":
    nombre = input("Ingresa tu nombre: ")
    cliente = ClienteDamas(nombre, 'localhost', 5555)

    recibir_hilo = threading.Thread(target=cliente.recibir_estado)
    recibir_hilo.start()

    while True:
        movimiento = input("Ingresa tu movimiento ('salir' para salir): ")
        cliente.enviar_movimiento(movimiento)
        if movimiento.lower() == "salir":
            break




