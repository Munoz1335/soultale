"""Inicia pygame y crea la ventana, el reloj y las fuentes.

Cualquier módulo que dibuje o suene debe importar este primero.
"""
import pygame

from config import ALTO, ANCHO, TITULO

pygame.mixer.pre_init(22050, -16, 1, 512)  # debe ir antes de pygame.init()
pygame.init()
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(TITULO)
clock = pygame.time.Clock()

MONO = "couriernew,consolas,dejavusansmono,monospace"
F = pygame.font.SysFont(MONO, 22, bold=True)
FP = pygame.font.SysFont(MONO, 18, bold=True)
FG = pygame.font.SysFont(MONO, 72, bold=True)
