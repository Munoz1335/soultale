"""Teclas del juego y lectura del movimiento."""
import pygame

DIRS = {pygame.K_LEFT: -1, pygame.K_a: -1, pygame.K_UP: -1, pygame.K_w: -1,
        pygame.K_RIGHT: 1, pygame.K_d: 1, pygame.K_DOWN: 1, pygame.K_s: 1}


def vector_teclado():
    """Devuelve (dx, dy) con -1, 0 o 1 según las flechas o WASD que estén pulsadas."""
    k = pygame.key.get_pressed()
    dx = (k[pygame.K_RIGHT] or k[pygame.K_d]) - (k[pygame.K_LEFT] or k[pygame.K_a])
    dy = (k[pygame.K_DOWN] or k[pygame.K_s]) - (k[pygame.K_UP] or k[pygame.K_w])
    return dx, dy
