import tkinter as tk

class TableroDamas:
    def __init__(self, root):
        self.root = root
        self.root.title("Tablero de Damas")
        
        self.casillas = [[None] * 8 for _ in range(8)]
        self.jugador_actual = "blanco"
        self.piezas = {}  # Diccionario para rastrear las piezas en el tablero
        self.crear_tablero()

    def crear_tablero(self):
        for i in range(8):
            for j in range(8):
                color = "white" if (i + j) % 2 == 0 else "black"
                casilla = tk.Canvas(self.root, width=50, height=50, bg=color, borderwidth=0, highlightthickness=0)
                casilla.grid(row=i, column=j)
                casilla.bind("<Button-1>", lambda event, row=i, col=j: self.casilla_clic(row, col))
                self.casillas[i][j] = casilla

        # Agregar piezas iniciales al tablero
        self.iniciar_piezas()

    def iniciar_piezas(self):
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 != 0:
                    self.crear_pieza(i, j, "negro")

        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 != 0:
                    self.crear_pieza(i, j, "blanco")

    def crear_pieza(self, fila, columna, jugador):
        pieza = tk.Canvas(self.root, width=50, height=50, bg="gray", borderwidth=0, highlightthickness=0)
        pieza.grid(row=fila, column=columna)
        pieza.create_oval(10, 10, 40, 40, fill="black" if jugador == "negro" else "white")  # Dibujar un círculo como representación de la pieza
        pieza.bind("<Button-1>", lambda event, row=fila, col=columna: self.pieza_clic(row, col))
        self.piezas[(fila, columna)] = {"jugador": jugador, "canvas": pieza}

    def pieza_clic(self, fila, columna):
        if self.jugador_actual == self.piezas[(fila, columna)]["jugador"]:
            print(f"Pieza clic: Fila {fila + 1}, Columna {columna + 1}, Jugador: {self.jugador_actual}")

    def casilla_clic(self, fila, columna):
        print(f"Casilla clic: Fila {fila + 1}, Columna {columna + 1}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TableroDamas(root)
    root.mainloop()





