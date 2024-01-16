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
    
    def manejar_eventos_raton(self, event):
        if event.type == MOUSEBUTTONDOWN:
            fila, columna = self.obtener_posicion_clic(event)
            if self.tablero_damas.ficha_seleccionada is None:
                self.tablero_damas.seleccionar_ficha(fila, columna)
            else:
                self.tablero_damas.mover_ficha(fila, columna)

    def obtener_posicion_clic(self, event):
        fila = event.pos[1] // ANCHO_CASILLA
        columna = event.pos[0] // ANCHO_CASILLA
        return fila, columna

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
    
    def dibujar_movimientos_validos(self, fila, columna):
        color_contorno = AZUL if self.tablero_damas.turno_actual == 2 else ROJO
        pygame.draw.circle(self.ventana, color_contorno, (columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 2 + 5, 3)
        movimientos_validos = self.tablero_damas.calcular_movimientos_validos(fila, columna)
        for movimiento in movimientos_validos:
            nueva_fila, nueva_columna = movimiento
            color_circulo = AMARILLO
            pygame.draw.circle(self.ventana, color_circulo, (nueva_columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, nueva_fila * ANCHO_CASILLA + ANCHO_CASILLA // 2), ANCHO_CASILLA // 2 - 5)
    
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
            if self.tablero_damas.ficha_seleccionada is not None:
                fila, columna = self.tablero_damas.ficha_seleccionada
                self.dibujar_movimientos_validos(fila, columna)
            self.mostrar_texto(f"Turno del Jugador: {self.tablero_damas.turno_actual}", (10, DIMENSION_VENTANA[1] - 40))
            pygame.display.flip()
            self.reloj.tick(60)

if __name__ == "__main__":
    juego_visual = TableroDamasVisual()
    juego_visual.ejecutar_juego()
