import socket
import tkinter as tk
import threading

class ClienteDamas:
    def __init__(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect(("127.0.0.1", 5555))

        self.root = tk.Tk()
        self.root.title("Juego de Damas - Cliente")

        self.jugador = self.cliente.recv(1024).decode()
        print(f"{self.jugador}")

        # Configurar la interfaz gráfica
        self.crear_tablero()

        # Iniciar el hilo para recibir actualizaciones del servidor
        threading.Thread(target=self.recibir_actualizaciones, daemon=True).start()

        self.root.mainloop()

    def crear_tablero(self):
        self.lienzo = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.lienzo.pack()

        self.casillas = [[None] * 8 for _ in range(8)]

        for fila in range(8):
            for columna in range(8):
                color = "white" if (fila + columna) % 2 == 0 else "black"
                x1, y1 = columna * 50, fila * 50
                x2, y2 = x1 + 50, y1 + 50
                casilla = self.lienzo.create_rectangle(x1, y1, x2, y2, fill=color, tags="casilla")
                self.casillas[fila][columna] = casilla

        self.iniciar_piezas()

    def iniciar_piezas(self):
        for fila in range(3):
            for columna in range(8):
                if (fila + columna) % 2 != 0:
                    self.crear_pieza(fila, columna, "A")

        for fila in range(5, 8):
            for columna in range(8):
                if (fila + columna) % 2 != 0:
                    self.crear_pieza(fila, columna, "blanco")

    def crear_pieza(self, fila, columna, jugador):
        x1, y1 = columna * 50, fila * 50
        x2, y2 = x1 + 50, y1 + 50
        color_ficha = "red" if jugador == "A" else "blue"
        pieza = self.lienzo.create_oval(x1+5, y1+5, x2-5, y2-5, fill=color_ficha, tags="pieza")
        self.casillas[fila][columna] = {"jugador": jugador, "pieza": pieza}

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

