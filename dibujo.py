"""Funciones de dibujo: texto, barras, corazón y monitores."""
import math

import pygame

from config import BLANCO, ROJO
from motor import F, FG, screen

HEART = [(16 * math.sin(t) ** 3,
          -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)))
         for t in (i * 0.2 for i in range(32))]


def texto(s, x, y, color=BLANCO, fuente=F, centro=False):
    if not s:
        return
    img = fuente.render(s, True, color)
    screen.blit(img, img.get_rect(center=(x, y)) if centro else (x, y))


def medidor(x, y, w, h, frac, color, fondo=(70, 0, 0)):
    pygame.draw.rect(screen, fondo, (x, y, w, h))
    pygame.draw.rect(screen, color, (x, y, int(w * max(0, min(1, frac))), h))


_glifos = {}


def glifo(ch, color):
    if (ch, color) not in _glifos:
        _glifos[(ch, color)] = F.render(ch, True, color)
    return _glifos[(ch, color)]


def corazon(x, y, color=ROJO, e=0.55):
    pygame.draw.polygon(screen, color, [(x + a * e, y + b * e) for a, b in HEART])


def monitor(cx, cy, color, simbolo, ojo):
    pygame.draw.rect(screen, color, (cx - 90, cy - 70, 180, 140), 6, border_radius=16)
    for dx in (-40, 40):
        pygame.draw.circle(screen, ojo, (cx + dx, cy - 35), 10)
    g = FG.render(simbolo, True, color)
    screen.blit(g, g.get_rect(center=(cx, cy + 20)))
