import socket
import threading

class ServerDamas:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("0.0.0.0", 5555))
        self.server.listen(2)
        print("Esperando conexiones...")

        self.clients = []
        self.addresses = []

        self.accept_connections()

    def accept_connections(self):
        while len(self.clients) < 2:
            try:
                client, address = self.server.accept()
                print(f"Conexión aceptada desde {address}")
                self.clients.append(client)
                self.addresses.append(address)

                threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()
            except (ConnectionResetError, socket.error) as e:
                print(f"Error al aceptar conexión: {e}")

        print("Dos jugadores conectados. Iniciando el juego.")

        # Solicitar nombres a los jugadores
        for client in self.clients:
            self.send_message(client, "Ingrese su nombre:")
            name = self.receive_message(client)
            print(f"Nombre de jugador {self.clients.index(client) + 1}: {name}")

        # Aquí puedes enviar un mensaje a ambos jugadores para indicar que el juego ha comenzado.

    def handle_client(self, client):
        try:
            while True:
                data = self.receive_message(client)
                if not data:
                    break

                # Puedes agregar lógica adicional aquí según los mensajes recibidos

        except (ConnectionResetError, socket.error) as e:
            print(f"Error en la conexión con {client.getpeername()}: {e}")
            self.clients.remove(client)
            self.send_message(client, "Se ha producido un error en la conexión. Adiós.")
            client.close()

        finally:
            if client in self.clients:
                self.clients.remove(client)
                print(f"{client.getpeername()} desconectado.")
                if len(self.clients) > 0:
                    remaining_client = self.clients[0]
                    remaining_client.send("El otro jugador se ha desconectado. Adiós.".encode())
                    self.clients.remove(remaining_client)
                    remaining_client.close()

    def send_message(self, client, message):
        try:
            client.send(message.encode())
        except (ConnectionResetError, socket.error) as e:
            print(f"Error al enviar mensaje: {e}")

    def receive_message(self, client):
        try:
            data = client.recv(1024)
            return data.decode()
        except (ConnectionResetError, socket.error) as e:
            print(f"Error al recibir mensaje: {e}")
            return None

if __name__ == "__main__":
    server = ServerDamas()










