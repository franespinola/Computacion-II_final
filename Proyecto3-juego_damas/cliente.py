import socket
import tkinter as tk
import threading

class ClienteDamas:
    def __init__(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect(("127.0.0.1", 5555))

        self.root = tk.Tk()
        self.root.title("Juego de Damas - Cliente")

        self.color = self.cliente.recv(1024).decode()
        print(f"Eres el jugador {self.color}")

        # Configurar la interfaz gráfica
        self.crear_tablero()

        # Iniciar el hilo para recibir actualizaciones del servidor
        threading.Thread(target=self.recibir_actualizaciones, daemon=True).start()

        self.root.mainloop()

    def crear_tablero(self):
        # Configurar la interfaz gráfica del tablero
        # ...

        # Configurar eventos de clic en las casillas del tablero
        # ...
        pass
    def enviar_movimiento(self, origen, destino):
        movimiento = f"{origen[0]},{origen[1]},{destino[0]},{destino[1]}"
        self.cliente.send(movimiento.encode())
        
    def recibir_actualizaciones(self):
        while True:
            try:
                data = self.cliente.recv(1024).decode()
                if not data:
                    break

                # Procesar la actualización del tablero y reflejarla en la interfaz gráfica
                # ...
            except Exception as e:
                print(e)
                break

if __name__ == "__main__":
    cliente = ClienteDamas()

