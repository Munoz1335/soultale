"""SOUL.EXE - Punto de entrada del juego.

Jugar:                                    py main.py
Demo automática (ideal para grabar):      py main.py --demo
"""
import sys

import pygame

from bot import Bot
from config import FPS
from juego import Juego
from motor import clock


def main():
    demo = "--demo" in sys.argv
    juego = Juego()
    if demo:
        juego.bot = Bot()
    while True:
        dt = min(clock.tick(FPS) / 1000, 0.05)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and not demo:
                juego.tecla(ev.key)
        if demo:
            juego.bot.actualizar(juego, dt)
        juego.actualizar(dt)
        juego.dibujar()
        pygame.display.flip()


if __name__ == "__main__":
    main()
