class TableroDamas:
    def __init__(self):
        self.estado = None
        self.inicializar_tablero()

    def inicializar_tablero(self):
        self.estado = [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 0]
        ]

    def mostrar_tablero(self):
        for fila in self.estado:
            print(fila)

    def obtener_pieza(self, fila, columna):
        return self.estado[fila][columna]

    def mover_pieza(self, fila_origen, columna_origen, fila_destino, columna_destino):
        # Mueve la pieza en el tablero
        self.estado[fila_destino][columna_destino] = self.estado[fila_origen][columna_origen]
        self.estado[fila_origen][columna_origen] = 0  # La casilla original queda vacía

    def validar_movimiento(self, jugador, fila_origen, columna_origen, fila_destino, columna_destino):
        print(f"Validando movimiento: Jugador {jugador}, Origen ({fila_origen}, {columna_origen}), Destino ({fila_destino}, {columna_destino})")
        if self.obtener_pieza(fila_origen, columna_origen) == jugador:
            if 0 <= fila_destino < 8 and 0 <= columna_destino < 8:
                # Verifica si la casilla de destino está vacía
                if self.obtener_pieza(fila_destino, columna_destino) == 0:
                    # Movimiento diagonal simple
                    if abs(fila_destino - fila_origen) == 1 and abs(columna_destino - columna_origen) == 1:
                        # Fichas rojas solo pueden avanzar hacia arriba (filas decrecientes)
                        if jugador == 1 and fila_destino < fila_origen:
                            return False
                        # Fichas azules solo pueden avanzar hacia arriba (filas decrecientes)
                        elif jugador == 2 and fila_destino > fila_origen:
                            return False
                        return True
                    # Movimiento diagonal para captura (salto)
                    elif abs(fila_destino - fila_origen) == 2 and abs(columna_destino - columna_origen) == 2:
                        fila_intermedia = (fila_destino + fila_origen) // 2
                        columna_intermedia = (columna_destino + columna_origen) // 2
                        # Verifica si hay una pieza enemiga en la casilla intermedia
                        if (
                            self.obtener_pieza(fila_intermedia, columna_intermedia) != jugador
                            and self.obtener_pieza(fila_intermedia, columna_intermedia) != 0
                            and (
                                (jugador == 1 and fila_intermedia < fila_destino)
                                or (jugador == 2 and fila_intermedia > fila_destino)
                            )
                        ):
                            return True
        return False



    def realizar_movimiento(self, jugador, fila_origen, columna_origen, fila_destino, columna_destino):
        print("Estado actual del tablero antes de mover la pieza:")
        self.mostrar_tablero()
        if self.validar_movimiento(jugador, fila_origen, columna_origen, fila_destino, columna_destino):
            self.mover_pieza(fila_origen, columna_origen, fila_destino, columna_destino)
            captura_realizada = self.eliminar_ficha_enemiga(jugador, fila_origen, columna_origen, fila_destino, columna_destino)
            if (jugador == 1 and fila_destino == 7) or (jugador == 2 and fila_destino == 0):
                print("Antes de coronar...")
                self.coronar_pieza(fila_destino, columna_destino)
                print("Después de coronar...")
            if captura_realizada and self.hay_capturas_disponibles(jugador, fila_destino, columna_destino):
                return self.realizar_movimiento(jugador, fila_destino, columna_destino, fila_destino + 2, columna_destino + 2)
            return True
        return False

    
    def eliminar_ficha_enemiga(self, jugador, fila_origen, columna_origen, fila_destino, columna_destino):
        # Calcula la posición intermedia
        fila_intermedia = (fila_destino + fila_origen) // 2
        columna_intermedia = (columna_destino + columna_origen) // 2

        # Verifica si hay una ficha enemiga en la posición intermedia
        if self.obtener_pieza(fila_intermedia, columna_intermedia) != jugador and self.obtener_pieza(fila_intermedia, columna_intermedia) != 0:
            # Verifica la dirección del movimiento
            if jugador == 1 and fila_intermedia < fila_destino:
                # Elimina la ficha enemiga
                self.estado[fila_intermedia][columna_intermedia] = 0
            elif jugador == 2 and fila_intermedia > fila_destino:
                # Elimina la ficha enemiga
                self.estado[fila_intermedia][columna_intermedia] = 0
            
    def coronar_pieza(self, fila, columna):
        # Corona la pieza en la posición especificada
        print(f"Coronando pieza en fila: {fila}, columna: {columna}")
        if self.obtener_pieza(fila, columna) == 1:
            self.estado[fila][columna] = 3  # Valor 3 para pieza coronada del jugador 1
        elif self.obtener_pieza(fila, columna) == 2:
            self.estado[fila][columna] = 4  # Valor 4 para pieza coronada del jugador 2
        print(f"Pieza coronada correctamente en fila: {fila}, columna: {columna}. Nuevo estado del tablero:")
        self.mostrar_tablero()
        
    def hay_capturas_disponibles(self, jugador, fila, columna):
    # Verifica si hay capturas disponibles para la pieza en la posición especificada
        for i in range(-2, 3, 4):  # Recorre las direcciones diagonal izquierda y diagonal derecha
            for j in range(-2, 3, 4):
                nueva_fila = fila + i
                nueva_columna = columna + j

                if 0 <= nueva_fila < 8 and 0 <= nueva_columna < 8:
                    if self.obtener_pieza(nueva_fila, nueva_columna) == 0:
                        # Casilla intermedia vacía, verifica si hay una pieza enemiga que pueda ser capturada
                        fila_intermedia = (fila + nueva_fila) // 2
                        columna_intermedia = (columna + nueva_columna) // 2
                        if self.obtener_pieza(fila_intermedia, columna_intermedia) != jugador and self.obtener_pieza(fila_intermedia, columna_intermedia) != 0:
                            return True
        return False