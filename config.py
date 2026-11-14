"""Constantes del juego (sin dependencias de pygame, para poder probarlas fácilmente)."""
ANCHO, ALTO = 800, 600
TITULO = "SOUL.EXE - Defiende la red"
FPS = 60

# Colores (R, G, B)
BLANCO, ROJO, AMARILLO, NARANJA = (255, 255, 255), (255, 0, 0), (255, 230, 0), (255, 140, 0)
VERDE, CIAN, GRIS = (0, 220, 90), (0, 220, 255), (110, 110, 110)

# Geometría: (x, y, ancho, alto)
CAJA = (40, 265, 720, 175)    # caja de texto y menús
ARENA = (250, 265, 300, 175)  # zona donde se esquivan los ataques

# Jugabilidad
VIDA_INICIAL = 30
DANO_BASE = 4    # HP que quita cada golpe (más 1 por cada nivel de enojo)
DURACION = 7.0   # segundos que dura cada ataque enemigo
