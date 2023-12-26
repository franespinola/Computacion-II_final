import socket
import threading

class ServidorDamas:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen(5)
        print(f"Servidor de damas escuchando en {self.host}:{self.port}")

    def manejar_cliente(self, cliente_socket):
        direccion = cliente_socket.getpeername()
        print("Nueva conexión desde {}:{}".format(direccion[0], direccion[1]))
        # Aquí puedes implementar la lógica para manejar la conexión con el cliente

    def esperar_conexiones(self):
        while True:
            cliente, _ = self.socket_servidor.accept() 
            cliente_thread = threading.Thread(target=self.manejar_cliente, args=(cliente,)) #aca en tarjet le indico a la funcion que voy a enviar el argumento(le paso cliente como argumnento)
            cliente_thread.start()

if __name__ == "__main__":
    servidor = ServidorDamas("127.0.0.1", 5555)
    servidor.esperar_conexiones()
