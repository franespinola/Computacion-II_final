import pygame
import sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from tablero import TableroDamas

# Definición de constantes
ANCHO_CASILLA = 80
FILA, COLUMNA = 8, 8
DIMENSION_VENTANA = ANCHO_CASILLA * COLUMNA, ANCHO_CASILLA * FILA

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
GRIS = (169, 169, 169)

class TableroDamasVisual:
    def __init__(self):
        pygame.init()
        self.ventana = pygame.display.set_mode(DIMENSION_VENTANA)
        pygame.display.set_caption("Juego de Damas")
        self.reloj = pygame.time.Clock()
        self.tablero_damas = TableroDamas()
        self.font = pygame.font.SysFont(None, 30)
        self.ficha_seleccionada = None
        self.turno_actual = 1  # Inicia el juego con el Jugador 1
    
    def cambiar_turno(self):
        # Cambia el turno entre Jugador 1 y Jugador 2
        print(f"Antes del cambio: Turno actual: {self.turno_actual}")
        self.turno_actual = 1 if self.turno_actual == 2 else 2
        print(f"Después del cambio: Turno actual: {self.turno_actual}")


    def dibujar_movimientos_validos(self, fila, columna):
        # Dibuja un círculo alrededor de la ficha seleccionada y los movimientos válidos
        pygame.draw.circle(self.ventana, ROJO, (columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 2 + 5, 3)

        for i in range(-2, 3, 4):
            for j in range(-2, 3, 4):
                nueva_fila = fila + i
                nueva_columna = columna + j

                if 0 <= nueva_fila < 8 and 0 <= nueva_columna < 8 and self.tablero_damas.validar_movimiento(self.turno_actual, fila, columna, nueva_fila, nueva_columna):
                    if self.tablero_damas.hay_capturas_disponibles(self.turno_actual, fila, columna) and not self.tablero_damas.validar_movimiento(self.turno_actual, fila, columna, nueva_fila, nueva_columna):
                        color_circulo = GRIS  # Cambia a color gris claro
                    else:
                        color_circulo = AZUL if self.turno_actual == 2 else ROJO  # Ajusta el color según el jugador

                    pygame.draw.circle(self.ventana, color_circulo, (nueva_columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, nueva_fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 2 - 5)

    def manejar_eventos_raton(self, event):
        if event.type == MOUSEBUTTONDOWN:
            fila = event.pos[1] // ANCHO_CASILLA
            columna = event.pos[0] // ANCHO_CASILLA

            if self.ficha_seleccionada is None:
                pieza = self.tablero_damas.obtener_pieza(fila, columna)
                if pieza == self.turno_actual:
                    self.ficha_seleccionada = (fila, columna)
            else:
                fila_origen, columna_origen = self.ficha_seleccionada
                if self.tablero_damas.validar_movimiento(self.turno_actual, fila_origen, columna_origen, fila, columna):
                    self.tablero_damas.realizar_movimiento(self.turno_actual, fila_origen, columna_origen, fila, columna)
                    self.ficha_seleccionada = None
                    self.cambiar_turno()  # Cambia al siguiente jugador
                else:
                    # Si no es un movimiento válido, verificar si hay una ficha temporal almacenada
                    if self.tablero_damas.obtener_pieza(fila, columna) == self.turno_actual:
                        self.ficha_seleccionada = (fila, columna)


    def dibujar_casillas(self):
        for fila in range(FILA):
            for columna in range(COLUMNA):
                color = BLANCO if (fila + columna) % 2 == 0 else NEGRO
                pygame.draw.rect(self.ventana, color, (columna * ANCHO_CASILLA, fila * ANCHO_CASILLA, ANCHO_CASILLA, ANCHO_CASILLA))

    def dibujar_piezas(self):
        for fila in range(FILA):
            for columna in range(COLUMNA):
                pieza = self.tablero_damas.obtener_pieza(fila, columna)
                if pieza == 1:  # Pieza roja
                    pygame.draw.circle(self.ventana, ROJO, (columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 2 - 5)
                elif pieza == 2:  # Pieza azul
                    pygame.draw.circle(self.ventana, AZUL, (columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 2 - 5)
                elif pieza == 3:  # Pieza coronada
                    pygame.draw.circle(self.ventana, GRIS, (columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 2 - 5)
                    pygame.draw.circle(self.ventana, ROJO, (columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 4 - 5)

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
