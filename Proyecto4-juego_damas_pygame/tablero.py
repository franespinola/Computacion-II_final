import pygame
import sys

# Definición de constantes
ANCHO_CASILLA = 80
FILA, COLUMNA = 8, 8
DIMENSION_VENTANA = ANCHO_CASILLA * FILA, ANCHO_CASILLA * COLUMNA

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
GRIS = (169, 169, 169)

class JuegoDamas:
    def __init__(self):
        pygame.init()
        self.ventana = pygame.display.set_mode(DIMENSION_VENTANA)
        pygame.display.set_caption("Juego de Damas")
        self.reloj = pygame.time.Clock()

        self.iniciar_tablero()
        self.iniciar_piezas()

    def iniciar_tablero(self):
        self.tablero = [[0] * COLUMNA for _ in range(FILA)]
        for fila in range(FILA):
            for columna in range(COLUMNA):
                color = BLANCO if (fila + columna) % 2 == 0 else NEGRO
                pygame.draw.rect(self.ventana, color, (columna * ANCHO_CASILLA, fila * ANCHO_CASILLA, ANCHO_CASILLA, ANCHO_CASILLA))

    def iniciar_piezas(self):
        for fila in range(3):
            for columna in range(COLUMNA):
                if (fila + columna) % 2 != 0:
                    self.tablero[fila][columna] = 1  # 1 representa una pieza roja

        for fila in range(5, 8):
            for columna in range(COLUMNA):
                if (fila + columna) % 2 != 0:
                    self.tablero[fila][columna] = 2  # 2 representa una pieza azul

    def dibujar_piezas(self):
        for fila in range(FILA):
            for columna in range(COLUMNA):
                if self.tablero[fila][columna] == 1:  # Placeholder para pieza roja
                    pygame.draw.circle(self.ventana, ROJO, (columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 2 - 5)
                elif self.tablero[fila][columna] == 2:  # Placeholder para pieza azul
                    pygame.draw.circle(self.ventana, AZUL, (columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 2 - 5)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.dibujar_piezas()  # Dibuja las piezas en el tablero
            pygame.display.flip()
            self.reloj.tick(60)

if __name__ == "__main__":
    juego = JuegoDamas()
    juego.run()
