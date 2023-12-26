import tkinter as tk

class TableroDamas:
    def __init__(self, root):
        self.root = root
        self.root.title("Tablero de Damas")
        
        self.casillas = [[None] * 8 for _ in range(8)]
        self.crear_tablero()

    def crear_tablero(self):
        for i in range(8):
            for j in range(8):
                color = "white" if (i + j) % 2 == 0 else "black"
                casilla = tk.Canvas(self.root, width=50, height=50, bg=color, borderwidth=0, highlightthickness=0)
                casilla.grid(row=i, column=j)
                casilla.bind("<Button-1>", lambda event, row=i, col=j: self.casilla_clic(row, col))
                self.casillas[i][j] = casilla

    def casilla_clic(self, row, col):
        print(f"Casilla clic: Fila {row + 1}, Columna {col + 1}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TableroDamas(root)
    root.mainloop()

