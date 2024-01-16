import socket
import threading
import pickle  # Usaremos pickle para serializar/deserializar objetos Python

class ServidorDamas:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientes = []
        self.partidas = {}
        self.iniciar_servidor()

    def iniciar_servidor(self):
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen(2)
        print(f"Servidor escuchando en {self.host}:{self.port}")

        while True:
            cliente, direccion = self.socket_servidor.accept()
            print(f"Conexión establecida con {direccion}")
            self.clientes.append(cliente)
            threading.Thread(target=self.gestionar_cliente, args=(cliente,)).start()

    def gestionar_cliente(self, cliente):
        nombre_cliente = pickle.loads(cliente.recv(1024))
        partida = self.unirse_a_partida(nombre_cliente, cliente)
        cliente.send(pickle.dumps(f"Bienvenido a la partida {partida}"))

        while True:
            try:
                mensaje = pickle.loads(cliente.recv(1024))
                if mensaje == "salir":
                    self.eliminar_partida(partida)
                    print(f"{nombre_cliente} abandonó la partida {partida}")
                    break
                else:
                    self.actualizar_estado(partida, mensaje)
                    estado_actualizado = self.obtener_estado(partida)
                    self.enviar_estado(partida, estado_actualizado)
            except Exception as e:
                print(f"Error con el cliente {nombre_cliente}: {str(e)}")
                break

    def unirse_a_partida(self, nombre_cliente, cliente):
        for partida, jugadores in self.partidas.items():
            if len(jugadores) < 2:
                jugadores.append((nombre_cliente, cliente))
                return partida
        nueva_partida = f"Partida-{len(self.partidas) + 1}"
        self.partidas[nueva_partida] = [(nombre_cliente, cliente)]
        return nueva_partida

    def eliminar_partida(self, partida):
        del self.partidas[partida]

    def actualizar_estado(self, partida, movimiento):
        # Lógica del juego: Actualizar el estado del juego según el movimiento recibido.
        # Puedes personalizar esto según tu juego específico.
        pass

    def obtener_estado(self, partida):
        # Lógica del juego: Obtener el estado actual de la partida.
        # Puedes personalizar esto según tu juego específico.
        pass

    def enviar_estado(self, partida, estado):
        for jugador in self.partidas[partida]:
            try:
                jugador[1].send(pickle.dumps(estado))
            except Exception as e:
                print(f"Error al enviar estado a {jugador[0]}: {str(e)}")
                self.eliminar_partida(partida)

if __name__ == "__main__":
    servidor = ServidorDamas('localhost', 5555)












