"""Jugador automático: sirve para grabar una demo sin tocar el teclado.  Uso: py main.py --demo"""
import math

import pygame

DIRECCIONES = ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
PAUSAS = {"titulo": 2.0, "fin": 4.0, "mensaje": 1.6, "actuar": 1.4}  # segundos de espera por estado


class Bot:
    def __init__(self):
        self.espera = 0.0

    @staticmethod
    def accion(j):
        """Qué botón del menú elegir: 0 ATACAR, 1 ACTUAR, 2 OBJETO, 3 PERDONAR."""
        if j.seg >= 100:
            return 3
        if j.hp <= 12 and j.items:
            return 2
        if j.idx == 1 and j.ehp == j.e["hp"]:  # ataca una vez al TROYANO para mostrar la barra
            return 0
        return 1

    def actualizar(self, j, dt):
        """Decide qué tecla 'pulsar' según el estado del juego. Se llama una vez por fotograma."""
        s = j.estado
        if s == "esquiva":
            return
        if s == "barra":  # pulsar Z justo cuando el cursor pasa por el centro
            if abs(j.cx - 400) < 16:
                j.tecla(pygame.K_z)
            return
        leyendo = s == "mensaje" and j.n < len(j.txt)
        self.espera = 0.0 if leyendo else self.espera + dt
        if self.espera < PAUSAS.get(s, 0.7):
            return
        self.espera = 0.0
        if s == "menu":
            j.tecla(pygame.K_z if j.sel == self.accion(j) else pygame.K_RIGHT)
        elif s == "actuar":
            qs = j.e["preguntas"]
            j.tecla(pygame.K_z if j.sub == qs[j.qi % len(qs)][2] else pygame.K_DOWN)
        else:
            j.tecla(pygame.K_z)

    def vector(self, j):
        """Elige hacia dónde mover el corazón para alejarse de las balas (se mira 1,2 s al futuro)."""
        r = j.rect.inflate(-28, -28)
        mejor, mejor_puntaje = (0, 0), -1e9
        for dx, dy in DIRECCIONES:
            minima, x, y = 60.0, j.px, j.py
            for t in (0.15, 0.3, 0.45, 0.6, 0.8, 1.0, 1.2):
                x = max(r.left, min(r.right, j.px + dx * 190 * t))
                y = max(r.top, min(r.bottom, j.py + dy * 190 * t))
                for b in j.bullets:
                    minima = min(minima, math.hypot(b.x + b.vx * t - x, b.y + b.vy * t - y))
            puntaje = minima - math.hypot(x - 400, y - 352) * 0.05  # prefiere quedarse cerca del centro
            if puntaje > mejor_puntaje:
                mejor, mejor_puntaje = (dx, dy), puntaje
        return mejor
