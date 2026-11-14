"""Sonidos generados por código (no hace falta ningún archivo de audio)."""
import pygame

import motor  # noqa: F401  (inicializa pygame y el mezclador)


def tono(freq, ms, vol):
    """Genera un pitido cuadrado. Devuelve None si no hay audio."""
    try:
        rate, _, canales = pygame.mixer.get_init()
        datos = b"".join((3000 if i * freq * 2 // rate % 2 == 0 else -3000)
                         .to_bytes(2, "little", signed=True) * canales
                         for i in range(rate * ms // 1000))
        s = pygame.mixer.Sound(buffer=datos)
        s.set_volume(vol)
        return s
    except Exception:
        return None


BLIP, GOLPE = tono(700, 30, 0.2), tono(110, 160, 0.4)


def sonar(s):
    if s:
        s.play()
