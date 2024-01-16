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
        self.ficha_seleccionada = None
        self.turno_actual = 1

    def inicializar_tablero(self):
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

    def cambiar_turno(self):
        self.turno_actual = 1 if self.turno_actual == 2 else 2

    def mostrar_tablero(self):
        for fila in self.estado:
            print(fila)

    def obtener_pieza(self, fila, columna):
        return self.estado[fila][columna]

    def mover_pieza(self, fila_origen, columna_origen, fila_destino, columna_destino):
        self.estado[fila_destino][columna_destino] = self.estado[fila_origen][columna_origen]
        self.estado[fila_origen][columna_origen] = self.VACIO
    
    def es_movimiento_salto(self, fila_origen, columna_origen, fila_destino, columna_destino):
        return abs(fila_destino - fila_origen) == 2 and abs(columna_destino - columna_origen) == 2
    
    def es_posicion_valida(self, fila, columna):
        return 0 <= fila < self.TAMANO_TABLERO and 0 <= columna < self.TAMANO_TABLERO
    
    def es_movimiento_diagonal(self, fila_origen, columna_origen, fila_destino, columna_destino):
        return abs(fila_destino - fila_origen) == 1 and abs(columna_destino - columna_origen) == 1

    def es_movimiento_adelante(self, jugador, fila_origen, fila_destino):
        if jugador in [self.REINA_1, self.REINA_2]:
            return True
        else:
            return (jugador == self.JUGADOR_1 and fila_destino > fila_origen) or (jugador == self.JUGADOR_2 and fila_destino < fila_origen)

    def eliminar_ficha_enemiga(self, jugador, fila_origen, columna_origen, fila_destino, columna_destino):
        fila_intermedia = (fila_destino + fila_origen) // 2
        columna_intermedia = (columna_destino + columna_origen) // 2
        self.estado[fila_intermedia][columna_intermedia] = self.VACIO
            
    def coronar_pieza(self, fila, columna):
        if self.obtener_pieza(fila, columna) == self.JUGADOR_1 and fila == self.TAMANO_TABLERO - 1:
            self.estado[fila][columna] = self.REINA_1
        elif self.obtener_pieza(fila, columna) == self.JUGADOR_2 and fila == 0:
            self.estado[fila][columna] = self.REINA_2 
        print("Estado actual del tablero después de coronar la pieza:")
        self.mostrar_tablero()
    
    #me fijo en realizar_movimiento para la captura multiple
    def validar_movimiento(self, jugador, fila_origen, columna_origen, fila_destino, columna_destino):
        pieza = self.obtener_pieza(fila_origen, columna_origen)
        if pieza in [self.JUGADOR_1, self.REINA_1] if jugador == 1 else pieza in [self.JUGADOR_2, self.REINA_2]:
            if self.es_posicion_valida(fila_destino, columna_destino) and self.obtener_pieza(fila_destino, columna_destino) == self.VACIO:
                if pieza in [self.REINA_1, self.REINA_2] and self.es_movimiento_valido_reina(jugador, fila_origen, columna_origen, fila_destino, columna_destino):
                    return True
                elif self.es_movimiento_diagonal(fila_origen, columna_origen, fila_destino, columna_destino) and self.es_movimiento_adelante(jugador, fila_origen, fila_destino):
                    return True
                elif self.es_movimiento_salto(fila_origen, columna_origen, fila_destino, columna_destino):
                    return self.validar_movimiento_captura(jugador, fila_origen, columna_origen, fila_destino, columna_destino)
        return False
    
    #me fijo en realizar_movimiento para la captura multiple
    def es_movimiento_valido_reina(self, jugador, fila_origen, columna_origen, fila_destino, columna_destino):
        if abs(fila_destino - fila_origen) != abs(columna_destino - columna_origen):
            return False
        fila_paso = 1 if fila_destino > fila_origen else -1
        columna_paso = 1 if columna_destino > columna_origen else -1
        fila_actual, columna_actual = fila_origen + fila_paso, columna_origen + columna_paso
        while fila_actual != fila_destino and columna_actual != columna_destino:
            pieza_actual = self.obtener_pieza(fila_actual, columna_actual)
            if pieza_actual != self.VACIO:
                if (jugador == 1 or jugador == self.REINA_1) and pieza_actual in [self.JUGADOR_1, self.REINA_1]:
                    return False
                elif (jugador == 2 or jugador == self.REINA_2) and pieza_actual in [self.JUGADOR_2, self.REINA_2]:
                    return False
                if self.obtener_pieza(fila_actual + fila_paso, columna_actual + columna_paso) != self.VACIO:
                    return False
            fila_actual += fila_paso
            columna_actual += columna_paso
        return True

    def validar_movimiento_captura(self, jugador, fila_origen, columna_origen, fila_destino, columna_destino):
        fila_intermedia = (fila_destino + fila_origen) // 2
        columna_intermedia = (columna_destino + columna_origen) // 2
        pieza_intermedia = self.obtener_pieza(fila_intermedia, columna_intermedia)
        pieza = self.obtener_pieza(fila_origen, columna_origen)
        if pieza in [self.REINA_1, self.REINA_2]:
            if jugador == 1 or jugador == self.REINA_1:
                if pieza_intermedia in [self.JUGADOR_2, self.REINA_2]:
                    return True
            elif jugador == 2 or jugador == self.REINA_2:
                if pieza_intermedia in [self.JUGADOR_1, self.REINA_1]:
                    return True
        else:
            if jugador == 1:
                if pieza_intermedia in [self.JUGADOR_2, self.REINA_2] and fila_intermedia < fila_destino:
                    return True
            elif jugador == 2:
                if pieza_intermedia in [self.JUGADOR_1, self.REINA_1] and fila_intermedia > fila_destino:
                    return True
        return False
    
    def calcular_movimientos_validos(self, fila, columna):
        movimientos_validos = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue  # No considerar la casilla actual
                nueva_fila = fila + i
                nueva_columna = columna + j
                while 0 <= nueva_fila < 8 and 0 <= nueva_columna < 8:
                    if self.validar_movimiento(self.turno_actual, fila, columna, nueva_fila, nueva_columna):
                        movimientos_validos.append((nueva_fila, nueva_columna))
                    nueva_fila += i
                    nueva_columna += j
        return movimientos_validos
    
    def realizar_movimiento(self, jugador, fila_origen, columna_origen, fila_destino, columna_destino):
        if self.validar_movimiento(jugador, fila_origen, columna_origen, fila_destino, columna_destino):
            pieza = self.obtener_pieza(fila_origen, columna_origen)
            self.mover_pieza(fila_origen, columna_origen, fila_destino, columna_destino)
            if pieza in [self.REINA_1, self.REINA_2] and abs(fila_destino - fila_origen) > 2:
                self.eliminar_fichas_enemigas_reina(jugador, fila_origen, columna_origen, fila_destino, columna_destino)
                if self.hay_capturas_disponibles_reina(jugador, fila_destino, columna_destino):
                    return True
            elif abs(fila_destino - fila_origen) == 2:
                self.eliminar_ficha_enemiga(jugador, fila_origen, columna_origen, fila_destino, columna_destino)
                if self.hay_capturas_disponibles(jugador, fila_destino, columna_destino):
                    return True
            if (jugador == 1 and fila_destino == 7) or (jugador == 2 and fila_destino == 0):
                self.coronar_pieza(fila_destino, columna_destino)
            return True
        return False
    
    def eliminar_fichas_enemigas_reina(self, jugador, fila_origen, columna_origen, fila_destino, columna_destino):
        fila_paso = 1 if fila_destino > fila_origen else -1
        columna_paso = 1 if columna_destino > columna_origen else -1
        fila_actual, columna_actual = fila_origen + fila_paso, columna_origen + columna_paso
        while fila_actual != fila_destino and columna_actual != columna_destino:
            pieza_actual = self.obtener_pieza(fila_actual, columna_actual)
            if pieza_actual != self.VACIO:
                if jugador == 1 or jugador == self.REINA_1:
                    if pieza_actual in [self.JUGADOR_2, self.REINA_2]:
                        self.estado[fila_actual][columna_actual] = self.VACIO
                elif jugador == 2 or jugador == self.REINA_2:
                    if pieza_actual in [self.JUGADOR_1, self.REINA_1]:
                        self.estado[fila_actual][columna_actual] = self.VACIO
            fila_actual += fila_paso
            columna_actual += columna_paso

    def hay_capturas_disponibles_reina(self, jugador, fila, columna):
        for fila_paso in [-1, 1]:
            for columna_paso in [-1, 1]:
                fila_actual, columna_actual = fila + fila_paso, columna + columna_paso
                while 0 <= fila_actual < self.TAMANO_TABLERO and 0 <= columna_actual < self.TAMANO_TABLERO:
                    pieza_actual = self.obtener_pieza(fila_actual, columna_actual)
                    if pieza_actual != self.VACIO:
                        if jugador == 1 or jugador == self.REINA_1:
                            if pieza_actual in [self.JUGADOR_2, self.REINA_2] and 0 <= fila_actual + fila_paso < self.TAMANO_TABLERO and 0 <= columna_actual + columna_paso < self.TAMANO_TABLERO and self.obtener_pieza(fila_actual + fila_paso, columna_actual + columna_paso) == self.VACIO:
                                return True
                        elif jugador == 2 or jugador == self.REINA_2:
                            if pieza_actual in [self.JUGADOR_1, self.REINA_1] and 0 <= fila_actual + fila_paso < self.TAMANO_TABLERO and 0 <= columna_actual + columna_paso < self.TAMANO_TABLERO and self.obtener_pieza(fila_actual + fila_paso, columna_actual + columna_paso) == self.VACIO:
                                return True
                    fila_actual += fila_paso
                    columna_actual += columna_paso
        return False
    
    def hay_capturas_disponibles(self, jugador, fila, columna):
        for i in range(-2, 3, 4):
            for j in range(-2, 3, 4):
                nueva_fila = fila + i
                nueva_columna = columna + j
                if 0 <= nueva_fila < self.TAMANO_TABLERO and 0 <= nueva_columna < self.TAMANO_TABLERO:
                    if self.validar_movimiento(jugador, fila, columna, nueva_fila, nueva_columna):
                        return True
        return False
    
    def seleccionar_ficha(self, fila, columna):
        pieza = self.obtener_pieza(fila, columna)
        if pieza == self.turno_actual or (self.turno_actual == 1 and pieza == self.REINA_1) or (self.turno_actual == 2 and pieza == self.REINA_2):
            self.ficha_seleccionada = (fila, columna)
            self.captura_en_turno = False  # Inicializa la variable de captura en el turno
            self.ficha_captura = None  # Inicializa la ficha que realizó la captura
        else:
            self.ficha_seleccionada = None  # Deselecciona la ficha actualmente seleccionada

    def mover_ficha(self, fila, columna):
        fila_origen, columna_origen = self.ficha_seleccionada
        if self.validar_movimiento(self.turno_actual, fila_origen, columna_origen, fila, columna):
            self.realizar_movimiento(self.turno_actual, fila_origen, columna_origen, fila, columna)
            pieza = self.obtener_pieza(fila, columna)
            if abs(fila - fila_origen) == 2:  # Si el movimiento fue una captura
                self.captura_en_turno = True  # Marca que hubo una captura en este turno
                self.ficha_captura = (fila, columna)  # Almacena la ficha que realizó la captura
            self.ficha_seleccionada = None
            if pieza in [self.REINA_1, self.REINA_2]:  # Si la pieza es una reina
                if self.captura_en_turno:  # Si la reina realizó una captura
                    for direccion in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:  # Verifica todas las direcciones
                        nueva_fila = fila + direccion[0]
                        nueva_columna = columna + direccion[1]
                        if 0 <= nueva_fila < len(self.estado) and 0 <= nueva_columna < len(self.estado[0]):  # Verifica si la nueva posición está dentro del rango del tablero
                            if self.hay_capturas_disponibles(self.turno_actual, nueva_fila, nueva_columna):
                                return  # Si hay más capturas disponibles, no cambia el turno
                self.cambiar_turno()  # Cambia al siguiente jugador si la reina no realizó una captura
            elif not self.captura_en_turno or not self.hay_capturas_disponibles(self.turno_actual, fila, columna) or (fila, columna) != self.ficha_captura:
                self.cambiar_turno()  # Cambia al siguiente jugador solo si no hay más capturas disponibles, o si no hubo una captura en este turno, o si la ficha que se mueve no es la que realizó la captura
        else:
            self.seleccionar_ficha(fila, columna)  # Selecciona una nueva ficha si el movimiento no es válido
    