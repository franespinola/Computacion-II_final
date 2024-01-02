import socket
import threading

class ServidorDamas:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("0.0.0.0", 5555))
        self.server.listen(2)
        print("Esperando conexiones...")
        self.jugadores = {}
        self.tablero = [[0] * 8 for _ in range(8)]  # Representación del tablero

    def manejar_conexiones(self):
        while True:
            cliente, direccion = self.server.accept()
            print(f"Conexión aceptada desde {direccion}")
            self.asignar_color(cliente)

            # Inicia un hilo para manejar la conexión con el cliente
            threading.Thread(target=self.manejar_cliente, args=(cliente,), daemon=True).start()

    def asignar_color(self, cliente):
        if len(self.jugadores) == 0:
            self.jugadores[cliente] = "A"
        elif len(self.jugadores) == 1:
            self.jugadores[cliente] = "B"
        else:
            cliente.send("La partida está llena. Espere a que termine.".encode())
            cliente.close()

        cliente.send(f"Bienvenido!.Eres el jugador {self.jugadores[cliente]}".encode())

    def manejar_cliente(self, cliente):
        while True:
            try:
                data = cliente.recv(1024)
                if not data:
                    break

                # Procesar el movimiento del cliente y actualizar el tablero
                movimiento = data.decode()
                # Actualizar la lógica del tablero según el movimiento recibido
                # ...

                # Enviar actualizaciones del tablero a ambos jugadores
                self.enviar_actualizacion()
            except Exception as e:
                print(e)
                break

        print(f"Cliente {self.jugadores[cliente]} desconectado.")
        del self.jugadores[cliente]
        cliente.close()

    def enviar_actualizacion(self):
        # Enviar el estado actual del tablero a ambos jugadores
        # ...
        pass
if __name__ == "__main__":
    servidor = ServidorDamas()
    servidor.manejar_conexiones()


