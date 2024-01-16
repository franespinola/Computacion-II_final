class TableroDamas:
    
    JUGADOR_1 = 1
    JUGADOR_2 = 2
    REINA_1 = 3
    REINA_2 = 4
    VACIO = 0
    TAMANO_TABLERO = 8
    
    def __init__(self):
        self.estado = None
        self.inicializar_tablero()

    def inicializar_tablero(self):
        ''''
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
        '''
        self.estado = [
            [self.VACIO, self.JUGADOR_1, self.VACIO, self.JUGADOR_1, self.VACIO, self.JUGADOR_1, self.VACIO, self.JUGADOR_1],
            [self.JUGADOR_1, self.VACIO, self.JUGADOR_1, self.VACIO, self.JUGADOR_1, self.VACIO, self.JUGADOR_1, self.VACIO],
            [self.VACIO, self.JUGADOR_1, self.VACIO, self.JUGADOR_1, self.VACIO, self.JUGADOR_1, self.VACIO, self.JUGADOR_1],
            [self.VACIO, self.VACIO, self.VACIO, self.VACIO, self.VACIO, self.VACIO, self.VACIO, self.VACIO],
            [self.VACIO, self.VACIO, self.VACIO, self.VACIO, self.VACIO, self.VACIO, self.VACIO, self.VACIO],
            [self.JUGADOR_2, self.VACIO, self.JUGADOR_2, self.VACIO, self.JUGADOR_2, self.VACIO, self.JUGADOR_2, self.VACIO],
            [self.VACIO, self.JUGADOR_2, self.VACIO, self.JUGADOR_2, self.VACIO, self.JUGADOR_2, self.VACIO, self.JUGADOR_2],
            [self.JUGADOR_2, self.VACIO, self.JUGADOR_2, self.VACIO, self.JUGADOR_2, self.VACIO, self.JUGADOR_2, self.VACIO]
        ]

    def mostrar_tablero(self):
        for fila in self.estado:
            print(fila)

    def obtener_pieza(self, fila, columna):
        return self.estado[fila][columna]

    def mover_pieza(self, fila_origen, columna_origen, fila_destino, columna_destino):
        self.estado[fila_destino][columna_destino] = self.estado[fila_origen][columna_origen]
        self.estado[fila_origen][columna_origen] = 0 

    def validar_movimiento(self, jugador, fila_origen, columna_origen, fila_destino, columna_destino):
        print(f"Validando movimiento desde ({fila_origen}, {columna_origen}) a ({fila_destino}, {columna_destino}) para el jugador {jugador}")
        pieza = self.obtener_pieza(fila_origen, columna_origen)
        if (jugador == 1 and pieza in [self.JUGADOR_1, self.REINA_1]) or (jugador == 2 and pieza in [self.JUGADOR_2, self.REINA_2]):
            print("La pieza en la posición de origen pertenece al jugador")
            if self.es_posicion_valida(fila_destino, columna_destino):
                print("La posición de destino es válida")
                if self.obtener_pieza(fila_destino, columna_destino) == self.VACIO:
                    print("La posición de destino está vacía")
                    if pieza in [self.REINA_1, self.REINA_2] and self.es_movimiento_valido_reina(fila_origen, columna_origen, fila_destino, columna_destino):
                        print("El movimiento es válido para una reina")
                        return True
                    elif self.es_movimiento_diagonal(fila_origen, columna_origen, fila_destino, columna_destino):
                        print("El movimiento es diagonal")
                        if self.es_movimiento_adelante(jugador, fila_origen, fila_destino):
                            print("El movimiento es hacia adelante")
                            return True
                    elif self.es_movimiento_salto(fila_origen, columna_origen, fila_destino, columna_destino):
                        print("El movimiento es un salto")
                        return self.validar_movimiento_captura(jugador, fila_origen, columna_origen, fila_destino, columna_destino)
        print("El movimiento no es válido")
        return False

    def es_posicion_valida(self, fila, columna):
        return 0 <= fila < self.TAMANO_TABLERO and 0 <= columna < self.TAMANO_TABLERO

    def es_movimiento_diagonal(self, fila_origen, columna_origen, fila_destino, columna_destino):
        return abs(fila_destino - fila_origen) == 1 and abs(columna_destino - columna_origen) == 1

    def es_movimiento_adelante(self, jugador, fila_origen, fila_destino):
        if jugador in [self.REINA_1, self.REINA_2]:
            return True # La reina puede moverse hacia adelante y hacia atrás
        else:
            return (jugador == self.JUGADOR_1 and fila_destino > fila_origen) or (jugador == self.JUGADOR_2 and fila_destino < fila_origen)

    def es_movimiento_valido_reina(self, fila_origen, columna_origen, fila_destino, columna_destino):
        print(f"Validando movimiento de reina desde ({fila_origen}, {columna_origen}) a ({fila_destino}, {columna_destino})")
        if abs(fila_destino - fila_origen) != abs(columna_destino - columna_origen):
            print("Movimiento no es diagonal")
            return False  # La reina solo puede moverse en diagonal
        fila_paso = 1 if fila_destino > fila_origen else -1
        columna_paso = 1 if columna_destino > columna_origen else -1
        fila_actual, columna_actual = fila_origen + fila_paso, columna_origen + columna_paso
        while fila_actual != fila_destino and columna_actual != columna_destino:
            if self.obtener_pieza(fila_actual, columna_actual) != self.VACIO:
                print(f"Pieza encontrada en el camino en ({fila_actual}, {columna_actual})")
                return False  # No puede haber ninguna pieza en el camino de la reina
            fila_actual += fila_paso
            columna_actual += columna_paso
        print("Movimiento de reina válido")
        return True

    
    def es_movimiento_salto(self, fila_origen, columna_origen, fila_destino, columna_destino):
        return abs(fila_destino - fila_origen) == 2 and abs(columna_destino - columna_origen) == 2
    
    def validar_movimiento_captura(self, jugador, fila_origen, columna_origen, fila_destino, columna_destino):
        fila_intermedia = (fila_destino + fila_origen) // 2
        columna_intermedia = (columna_destino + columna_origen) // 2
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
            if abs(fila_destino - fila_origen) == 2:
                self.eliminar_ficha_enemiga(jugador, fila_origen, columna_origen, fila_destino, columna_destino)
                if self.hay_capturas_disponibles(jugador, fila_destino, columna_destino):
                    return True  # Si hay más capturas disponibles, el turno no termina
            if (jugador == 1 and fila_destino == 7) or (jugador == 2 and fila_destino == 0):
                self.coronar_pieza(fila_destino, columna_destino)
            return True
        return False
    
    def eliminar_ficha_enemiga(self, jugador, fila_origen, columna_origen, fila_destino, columna_destino):
        fila_intermedia = (fila_destino + fila_origen) // 2
        columna_intermedia = (columna_destino + columna_origen) // 2
        self.estado[fila_intermedia][columna_intermedia] = self.VACIO
            
    def coronar_pieza(self, fila, columna):
        if self.obtener_pieza(fila, columna) == self.JUGADOR_1 and fila ==self.TAMANO_TABLERO - 1:
            self.estado[fila][columna] = self.REINA_1
        elif self.obtener_pieza(fila, columna) == self.JUGADOR_2 and fila == 0:
            self.estado[fila][columna] = self.REINA_2 
        print("Estado actual del tablero después de coronar la pieza:")
        self.mostrar_tablero()

    def hay_capturas_disponibles(self, jugador, fila, columna):
        for i in range(-2, 3, 4):
            for j in range(-2, 3, 4):
                nueva_fila = fila + i
                nueva_columna = columna + j
                if 0 <= nueva_fila < self.TAMANO_TABLERO and 0 <= nueva_columna < self.TAMANO_TABLERO:
                    if self.validar_movimiento(jugador, fila, columna, nueva_fila, nueva_columna):
                        return True
        return False