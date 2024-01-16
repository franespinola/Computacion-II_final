import pygame
import sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from tablero import TableroDamas

ANCHO_CASILLA = 80
FILA, COLUMNA = 8, 8
DIMENSION_VENTANA = ANCHO_CASILLA * COLUMNA, ANCHO_CASILLA * FILA

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 200)  
GRIS = (169, 169, 169)

PIEZA_ROJA = 1
PIEZA_AZUL = 2
DAMA_ROJA = 3
DAMA_AZUL = 4

class TableroDamasVisual:
    
    def __init__(self):
        pygame.init()
        self.ventana = pygame.display.set_mode(DIMENSION_VENTANA)
        pygame.display.set_caption("Juego de Damas")
        self.reloj = pygame.time.Clock()
        self.tablero_damas = TableroDamas()
        self.font = pygame.font.SysFont(None, 30)
        self.ficha_seleccionada = None
        self.turno_actual = 1  
    
    def cambiar_turno(self):
        self.turno_actual = 1 if self.turno_actual == 2 else 2

    def dibujar_movimientos_validos(self, fila, columna):
        color_contorno = AZUL if self.turno_actual == 2 else ROJO
        pygame.draw.circle(self.ventana, color_contorno, (columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 2 + 5, 3)

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue  # No dibujar la casilla actual
                nueva_fila = fila + i
                nueva_columna = columna + j
                while 0 <= nueva_fila < 8 and 0 <= nueva_columna < 8:
                    if self.tablero_damas.validar_movimiento(self.turno_actual, fila, columna, nueva_fila, nueva_columna):
                        color_circulo = AMARILLO
                        pygame.draw.circle(self.ventana, color_circulo, (nueva_columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, nueva_fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 2 - 5)
                    nueva_fila += i
                    nueva_columna += j

    def manejar_eventos_raton(self, event):
        if event.type == MOUSEBUTTONDOWN:
            fila, columna = self.obtener_posicion_clic(event)
            if self.ficha_seleccionada is None:
                self.seleccionar_ficha(fila, columna)
            else:
                self.mover_ficha(fila, columna)

    def obtener_posicion_clic(self, event):
        fila = event.pos[1] // ANCHO_CASILLA
        columna = event.pos[0] // ANCHO_CASILLA
        return fila, columna

    def seleccionar_ficha(self, fila, columna):
        pieza = self.tablero_damas.obtener_pieza(fila, columna)
        if pieza == self.turno_actual or (self.turno_actual == 1 and pieza == DAMA_ROJA) or (self.turno_actual == 2 and pieza == DAMA_AZUL):
            self.ficha_seleccionada = (fila, columna)
            self.captura_en_turno = False  # Inicializa la variable de captura en el turno
            self.ficha_captura = None  # Inicializa la ficha que realizó la captura
        else:
            self.ficha_seleccionada = None  # Deselecciona la ficha actualmente seleccionada

    def mover_ficha(self, fila, columna):
        fila_origen, columna_origen = self.ficha_seleccionada
        if self.tablero_damas.validar_movimiento(self.turno_actual, fila_origen, columna_origen, fila, columna):
            self.tablero_damas.realizar_movimiento(self.turno_actual, fila_origen, columna_origen, fila, columna)
            pieza = self.tablero_damas.obtener_pieza(fila, columna)
            if abs(fila - fila_origen) == 2:  # Si el movimiento fue una captura
                self.captura_en_turno = True  # Marca que hubo una captura en este turno
                self.ficha_captura = (fila, columna)  # Almacena la ficha que realizó la captura
            self.ficha_seleccionada = None
            if pieza in [DAMA_ROJA, DAMA_AZUL]:  # Si la pieza es una reina
                if self.captura_en_turno:  # Si la reina realizó una captura
                    for direccion in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:  # Verifica todas las direcciones
                        nueva_fila = fila + direccion[0]
                        nueva_columna = columna + direccion[1]
                        if 0 <= nueva_fila < len(self.tablero_damas.estado) and 0 <= nueva_columna < len(self.tablero_damas.estado[0]):  # Verifica si la nueva posición está dentro del rango del tablero
                            if self.tablero_damas.hay_capturas_disponibles(self.turno_actual, nueva_fila, nueva_columna):
                                return  # Si hay más capturas disponibles, no cambia el turno
                self.cambiar_turno()  # Cambia al siguiente jugador si la reina no realizó una captura
            elif not self.captura_en_turno or not self.tablero_damas.hay_capturas_disponibles(self.turno_actual, fila, columna) or (fila, columna) != self.ficha_captura:
                self.cambiar_turno()  # Cambia al siguiente jugador solo si no hay más capturas disponibles, o si no hubo una captura en este turno, o si la ficha que se mueve no es la que realizó la captura
        else:
            self.seleccionar_ficha(fila, columna)  # Selecciona una nueva ficha si el movimiento no es válido

    def dibujar_casillas(self):
        for fila in range(FILA):
            for columna in range(COLUMNA):
                color = BLANCO if (fila + columna) % 2 == 0 else NEGRO
                pygame.draw.rect(self.ventana, color, (columna * ANCHO_CASILLA, fila * ANCHO_CASILLA, ANCHO_CASILLA, ANCHO_CASILLA))

    def dibujar_piezas(self):
        for fila in range(FILA):
            for columna in range(COLUMNA):
                pieza = self.tablero_damas.obtener_pieza(fila, columna)
                if pieza == PIEZA_ROJA:
                    pygame.draw.circle(self.ventana, ROJO, (columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 2 - 5)
                elif pieza == PIEZA_AZUL: 
                    pygame.draw.circle(self.ventana, AZUL, (columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 2 - 5)
                elif pieza == DAMA_ROJA:
                    pygame.draw.circle(self.ventana, GRIS, (columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 2 - 5)
                    pygame.draw.circle(self.ventana, ROJO, (columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 4 - 5)
                elif pieza == DAMA_AZUL:
                    pygame.draw.circle(self.ventana, GRIS, (columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 2 - 5)
                    pygame.draw.circle(self.ventana, AZUL, (columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 4 - 5)
    
    def mostrar_texto(self, texto, posicion):
        texto_renderizado = self.font.render(texto, True, NEGRO)
        self.ventana.blit(texto_renderizado, posicion)

    def ejecutar_juego(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    self.manejar_eventos_raton(event)
            self.ventana.fill(BLANCO)
            self.dibujar_casillas()
            self.dibujar_piezas()
            if self.ficha_seleccionada is not None:
                fila, columna = self.ficha_seleccionada
                self.dibujar_movimientos_validos(fila, columna)
            self.mostrar_texto(f"Turno del Jugador: {self.turno_actual}", (10, DIMENSION_VENTANA[1] - 40))
            pygame.display.flip()
            self.reloj.tick(60)

if __name__ == "__main__":
    juego_visual = TableroDamasVisual()
    juego_visual.ejecutar_juego()
