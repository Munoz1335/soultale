"""Patrones de ataque. Son funciones puras: reciben datos y devuelven las balas (sin pygame)."""
import math
import random

from balas import Bala
from config import ARENA

PATRONES = ("lluvia", "disparo", "muro", "rescate")


def crear(patron, v, jugador, lado):
    """Devuelve (balas, segundos hasta el siguiente ataque).

    patron:  nombre del patrón ("jefe" elige uno al azar)
    v:       multiplicador de velocidad (sube con el enojo del enemigo)
    jugador: (x, y) del corazón
    lado:    -1 o 1, desde dónde sale el muro
    """
    x0, y0, w, h = ARENA
    px, py = jugador
    if patron == "jefe":
        patron = random.choice(PATRONES)
    balas = []
    if patron == "lluvia":  # arroba que cae del techo
        for _ in range(2):
            balas.append(Bala(random.uniform(x0 + 10, x0 + w - 10), y0, 0, 150 * v, "@"))
        return balas, 0.35 / v
    if patron == "disparo":  # 0 y 1 que apuntan al jugador
        a = math.atan2(py - y0, px - (x0 + w / 2))
        for d in (-0.4, 0, 0.4):
            balas.append(Bala(x0 + w / 2, y0, math.cos(a + d) * 160 * v, math.sin(a + d) * 160 * v,
                              random.choice("01")))
        return balas, 1.0 / v
    if patron == "rescate":  # monedas que cruzan de lado a lado
        lado_r = random.choice((-1, 1))
        for _ in range(2):
            balas.append(Bala(x0 if lado_r == 1 else x0 + w, random.uniform(y0 + 10, y0 + h - 10),
                              lado_r * 170 * v, 0, "$"))
        return balas, 0.5 / v
    hueco = random.randint(0, 5)  # muro de asteriscos con un hueco de 2 filas
    for i in range(7):
        if i not in (hueco, hueco + 1):
            balas.append(Bala(x0 if lado == 1 else x0 + w, y0 + h / 7 * (i + 0.5), lado * 130 * v, 0, "*"))
    return balas, 1.6 / v
