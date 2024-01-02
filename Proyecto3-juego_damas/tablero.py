import tkinter as tk

class TableroDamas:
    def __init__(self, root):
        self.root = root
        self.root.title("Tablero de Damas")
        
        self.casillas = [[None] * 8 for _ in range(8)]
        self.jugador_actual = "blanco"
        self.piezas = {}  # Diccionario para rastrear las piezas en el tablero
        self.casilla_seleccionada = None  # Almacena la casilla seleccionada para el movimiento
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
            # Almacena la casilla seleccionada para el movimiento
            self.casilla_seleccionada = (fila, columna)
        else:
            # Intenta realizar el movimiento si hay una casilla seleccionada
            if self.casilla_seleccionada:
                destino = (fila, columna)
                if self.es_movimiento_valido(self.casilla_seleccionada, destino):
                    self.realizar_movimiento(self.casilla_seleccionada, destino)
                    self.cambiar_turno()
                self.casilla_seleccionada = None

    def es_movimiento_valido(self, origen, destino):
        fila_origen, columna_origen = origen
        fila_destino, columna_destino = destino

        # Verifica si la casilla de destino está vacía
        if destino in self.piezas:
            return False

        # Verifica si el movimiento es diagonal
        if abs(fila_destino - fila_origen) != 1 or abs(columna_destino - columna_origen) != 1:
            return False

        # Verifica si las blancas solo se mueven hacia arriba y las negras hacia abajo
        if self.jugador_actual == "blanco" and fila_destino <= fila_origen:
            return False
        elif self.jugador_actual == "negro" and fila_destino >= fila_origen:
            return False

        return True

    def realizar_movimiento(self, origen, destino):
        # Mueve la pieza a la casilla de destino
        self.piezas[destino] = self.piezas[origen]
        del self.piezas[origen]

        fila_origen, columna_origen = origen
        fila_destino, columna_destino = destino

        # Promociona la pieza a dama si llega al extremo opuesto del tablero
        if self.promover_a_dama(destino):
            self.piezas[destino]["es_dama"] = True

        # Captura de piezas (movimiento en diagonal de dos casillas)
        if abs(fila_destino - fila_origen) == 2 and abs(columna_destino - columna_origen) == 2:
            # Calcula la posición de la pieza capturada
            fila_captura = (fila_destino + fila_origen) // 2
            columna_captura = (columna_destino + columna_origen) // 2
            posicion_captura = (fila_captura, columna_captura)

            # Verifica si hay una pieza en la posición intermedia y la elimina
            if posicion_captura in self.piezas:
                del self.piezas[posicion_captura]

        # Actualiza la interfaz gráfica para reflejar el movimiento
        self.actualizar_interfaz()



    def promover_a_dama(self, posicion):
        fila, _ = posicion
        if (self.jugador_actual == "blanco" and fila == 7) or (self.jugador_actual == "negro" and fila == 0):
            return True
        return False


    def actualizar_interfaz(self):
        # Actualiza la interfaz gráfica después de cada movimiento
        for fila in range(8):
            for columna in range(8):
                self.casillas[fila][columna].delete("all")  # Limpia la casilla
                if (fila, columna) in self.piezas:
                    jugador = self.piezas[(fila, columna)]["jugador"]
                    self.casillas[fila][columna].create_oval(10, 10, 40, 40, fill="black" if jugador == "negro" else "white")

    def casilla_clic(self, fila, columna):
        print(f"Casilla clic: Fila {fila + 1}, Columna {columna + 1}")

    def cambiar_turno(self):
        self.jugador_actual = "blanco" if self.jugador_actual == "negro" else "negro"

if __name__ == "__main__":
    root = tk.Tk()
    app = TableroDamas(root)
    root.mainloop()






