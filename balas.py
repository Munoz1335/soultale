"""Proyectiles que el jugador debe esquivar."""


class Bala:
    def __init__(self, x, y, vx, vy, ch):
        self.x, self.y = x, y     # posición (píxeles)
        self.vx, self.vy = vx, vy  # velocidad (píxeles por segundo)
        self.ch = ch              # carácter con el que se dibuja
