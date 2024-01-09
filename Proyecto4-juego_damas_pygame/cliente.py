import socket
import threading

class ClientDamas:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = self.connect_to_server()

        if self.connected:
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.send_messages()

    def connect_to_server(self):
        try:
            self.client.connect(("127.0.0.1", 5555))
            return True
        except ConnectionRefusedError as e:
            print("La sala está llena. Espere a que termine la partida.")
            return False

    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(1024)
                if not data:
                    break

                message = data.decode()
                print(message)

                if "Ingrese su nombre" in message:
                    name = input("Ingrese su nombre: ")
                    self.send_message(name)

            except ConnectionResetError as e:
                print(f"Error al recibir mensajes: {e}")
                break

    def send_messages(self):
        while True:
            try:
                message = input("Ingrese su mensaje: ")
                self.send_message(message)
            except ConnectionResetError as e:
                print(f"Error al enviar mensajes: {e}")
                break

    def send_message(self, message):
        try:
            self.client.send(message.encode())
        except ConnectionResetError as e:
            print(f"Error al enviar mensaje: {e}")

if __name__ == "__main__":
    client = ClientDamas()








