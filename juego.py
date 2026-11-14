"""Clase Juego: la máquina de estados del combate, las escenas de historia y las pantallas."""
import math
import random
import textwrap

import pygame

import patrones
from config import (AMARILLO, ARENA, BLANCO, CAJA, CIAN, DANO_BASE, DURACION, GRIS, NARANJA, ROJO, VERDE,
                    VIDA_INICIAL)
from controles import DIRS, vector_teclado
from dibujo import corazon, glifo, medidor, monitor, texto
from enemigos import CAST, ENEMIGOS
from historia import FIN_AGRESIVA, FIN_NEUTRAL, FIN_PACIFISTA, FINALES, PROLOGO
from motor import F, FG, FP, screen
from sonido import BLIP, GOLPE, sonar


class Juego:
    def __init__(self):
        self.estado, self.fin = "titulo", ""
        self.cur, self.tb = list(CAJA), CAJA
        self.rect = pygame.Rect(CAJA)
        self.txt, self.n, self.then, self.quien = "", 0.0, None, None
        self.cola, self.al_terminar, self.frase = [], None, ""
        self.sel = self.sub = 0
        self.shake = self.inv = self.t = self.cd = 0.0
        self.px = self.py = 0.0
        self.cx, self.lado, self.bullets = 100.0, 1, []
        self.bot = None  # si es un Bot, juega solo (modo demo)

    # ---------- historia: escenas de diálogo ----------
    def escena(self, lineas, al_terminar):
        self.cola, self.al_terminar = list(lineas), al_terminar
        self.siguiente_linea()

    def siguiente_linea(self):
        if not self.cola:
            return self.al_terminar()
        quien, txt = self.cola.pop(0)
        self.say(txt, self.siguiente_linea, quien)

    def nueva(self):
        self.hp = self.maxhp = VIDA_INICIAL
        self.idx = self.kills = 0
        self.items = [["Antivirus", 12, 2], ["Copia de seguridad", 25, 1]]
        self.sel = self.sub = 0
        self.preparar(PROLOGO)

    def preparar(self, previo=()):
        e = self.e = ENEMIGOS[self.idx]
        self.ehp, self.seg, self.enojo, self.qi = e["hp"], 0, 0, 0
        self.escena(list(previo) + [("NARRADOR", "* " + e["capitulo"])] + e["antes"], self.a_menu)

    def reintentar(self):
        e = self.e
        self.hp = self.maxhp
        self.ehp, self.seg, self.enojo, self.qi = e["hp"], 0, 0, 0
        self.a_menu()

    def dar_item(self):
        for it in self.items:
            if it[0] == "Antivirus":
                it[2] += 1
                return
        self.items.append(["Antivirus", 12, 1])

    def ganar(self, matado):
        e, n = self.e, self.e["nombre"]
        if matado:
            self.kills += 1
        if e.get("jefe"):
            return self.final(matado)
        self.hp = self.maxhp
        self.dar_item()
        primera = f"* Borraste a {n} sin entender cómo detenerlo." if matado else f"* ¡{n} fue neutralizado sin violencia!"
        lineas = ([("NARRADOR", primera)] + e["borrado" if matado else "salvo"] + e["despues"]
                  + [("NARRADOR", "* PUNTO DE CONTROL: tu HP se restaura y ganas un Antivirus.")])
        self.escena(lineas, self.siguiente)

    def siguiente(self):
        self.idx += 1
        self.preparar()

    def final(self, matado):
        if matado:
            ruta, lineas = "agresiva", FIN_AGRESIVA
        elif self.kills:
            ruta, lineas = "neutral", FIN_NEUTRAL
        else:
            ruta, lineas = "pacifista", FIN_PACIFISTA
        self.escena(lineas, lambda: self.terminar(ruta))

    def terminar(self, ruta):
        self.estado, self.fin = "fin", ruta

    # ---------- flujo del combate ----------
    def say(self, txt, then, quien=None):
        self.txt, self.n, self.then, self.quien = txt, 0.0, then, quien
        self.estado, self.tb = "mensaje", CAJA

    def flavor(self):
        n = self.e["nombre"]
        if self.seg >= 100:
            return f"* {n} ya no quiere atacar. Usa PERDONAR."
        if self.enojo:
            return f"* {n} está furioso. ¡Cuidado!"
        return random.choice(["* Tu red está en peligro.", "* Piensa antes de hacer clic.",
                              "* Hay código sospechoso en el aire."])

    def a_menu(self):
        self.estado, self.tb, self.quien = "menu", CAJA, None
        self.txt, self.n = self.flavor(), 0.0

    def elegir(self):
        self.sub = 0
        if self.sel == 0:
            self.estado, self.cx = "barra", 100.0
        elif self.sel == 1:
            self.estado = "actuar"
        elif self.sel == 2:
            if self.items:
                self.estado = "objeto"
            else:
                self.say("* No te quedan objetos.", self.a_menu)
        elif self.seg >= 100:
            self.ganar(False)
        else:
            self.say(f"* {self.e['nombre']} aún no se siente seguro. Usa ACTUAR primero.", self.iniciar_ataque)

    def golpear(self):
        dmg = max(2, round(30 * (1 - abs(self.cx - 400) / 300)))
        self.ehp -= dmg
        self.shake = 0.5
        sonar(GOLPE)
        if self.ehp <= 0:
            self.ganar(True)
        else:
            self.say(f"* Tu escaneo hace {dmg} de daño a {self.e['nombre']}.", self.iniciar_ataque)

    def responder(self):
        qs = self.e["preguntas"]
        _, _, bien, expl = qs[self.qi % len(qs)]
        self.qi += 1
        if self.sub == bien:
            paso = self.e.get("paso", 50)
            self.seg = min(100, self.seg + paso)
            self.say(f"¡Correcto! {expl} (SEGURIDAD +{paso}%)", self.iniciar_ataque)
        else:
            self.enojo = min(3, self.enojo + 1)
            self.say(f"¡Incorrecto! {expl}", self.iniciar_ataque)

    def usar(self):
        it = self.items[self.sub]
        cura = min(it[1], self.maxhp - self.hp)
        self.hp += cura
        it[2] -= 1
        if it[2] == 0:
            self.items.remove(it)
        self.say(f"* Usas {it[0]}. Recuperas {cura} HP.", self.iniciar_ataque)

    # ---------- ataque enemigo (esquivar) ----------
    def iniciar_ataque(self):
        self.estado, self.tb, self.quien = "esquiva", ARENA, None
        self.bullets, self.t, self.cd, self.inv = [], 0.0, 0.7, 0.0
        self.lado = random.choice((-1, 1))
        self.frase = random.choice(self.e["frases"])
        self.px, self.py = ARENA[0] + ARENA[2] / 2, ARENA[1] + ARENA[3] / 2

    def crear(self):
        """Pide a patrones.py las balas del siguiente ataque."""
        balas, self.cd = patrones.crear(self.e["patron"], 1 + 0.2 * self.enojo, (self.px, self.py), self.lado)
        self.bullets.extend(balas)

    def esquivar(self, dt):
        dx, dy = self.bot.vector(self) if self.bot else vector_teclado()
        if dx and dy:
            dx, dy = dx * 0.707, dy * 0.707
        lim = self.rect.inflate(-28, -28)
        self.px = max(lim.left, min(lim.right, self.px + dx * 190 * dt))
        self.py = max(lim.top, min(lim.bottom, self.py + dy * 190 * dt))
        self.t += dt
        self.cd -= dt
        self.inv -= dt
        if self.cd <= 0 and self.t < DURACION - 1.5:
            self.crear()
        for b in self.bullets:
            b.x += b.vx * dt
            b.y += b.vy * dt
            if self.inv <= 0 and math.hypot(b.x - self.px, b.y - self.py) < 11:
                self.hp = max(0, self.hp - DANO_BASE - self.enojo)
                self.inv = 1.0
                sonar(GOLPE)
        zona = pygame.Rect(ARENA).inflate(80, 80)
        self.bullets = [b for b in self.bullets if zona.collidepoint(int(b.x), int(b.y))]
        if self.hp <= 0:
            self.estado, self.fin = "fin", "derrota"
        elif self.t >= DURACION:
            self.a_menu()

    # ---------- entrada y actualizacion ----------
    def tecla(self, k):
        ok = k in (pygame.K_z, pygame.K_RETURN)
        atras = k == pygame.K_x
        d, s = DIRS.get(k, 0), self.estado
        if s == "titulo":
            if ok:
                self.nueva()
        elif s == "fin":
            if ok:
                self.reintentar() if self.fin == "derrota" else self.nueva()
        elif s == "mensaje":
            if ok and self.n < len(self.txt):
                self.n = len(self.txt)
            elif ok:
                self.then()
        elif s == "menu":
            self.sel = (self.sel + d) % 4
            if ok:
                self.elegir()
        elif s == "barra":
            if ok:
                self.golpear()
            elif atras:
                self.a_menu()
        elif s == "actuar":
            self.sub = (self.sub + d) % 3
            if ok:
                self.responder()
            elif atras:
                self.a_menu()
        elif s == "objeto":
            self.sub = (self.sub + d) % len(self.items)
            if ok:
                self.usar()
            elif atras:
                self.a_menu()

    def actualizar(self, dt):
        for i in range(4):  # la caja se encoge/expande suavemente
            self.cur[i] += (self.tb[i] - self.cur[i]) * min(1, dt * 14)
        self.rect = pygame.Rect([round(v) for v in self.cur])
        self.shake = max(0, self.shake - dt)
        if self.estado in ("menu", "mensaje") and self.n < len(self.txt):
            viejo = int(self.n)
            self.n = min(len(self.txt), self.n + 40 * dt)
            if int(self.n) != viejo:
                sonar(BLIP)
        elif self.estado == "barra":
            self.cx += 620 * dt
            if self.cx > 700:
                self.say("* Tu escaneo falló...", self.iniciar_ataque)
        elif self.estado == "esquiva":
            self.esquivar(dt)

    # ---------- dibujo ----------
    def escribir(self, dy=0):
        n, y = int(self.n), self.rect.top + 18 + dy
        for linea in textwrap.wrap(self.txt, 48):
            texto(linea[:max(0, n)], self.rect.left + 22, y)
            n -= len(linea) + 1
            y += 28

    def indicador(self):
        if self.estado == "mensaje" and self.n >= len(self.txt) and pygame.time.get_ticks() // 400 % 2:
            texto("v", self.rect.right - 38, self.rect.bottom - 34, GRIS)

    def enemigo(self):
        e = self.e
        cx = 400 + (random.randint(-6, 6) if self.shake > 0 else 0)
        cy = 135 + int(math.sin(pygame.time.get_ticks() / 400) * 6)
        monitor(cx, cy, e["color"], e["simbolo"], VERDE if self.seg >= 100 else ROJO if self.enojo else BLANCO)

    def hud(self):
        e = self.e
        texto(e["nombre"], 20, 18)
        texto("HP", 20, 54, GRIS, FP)
        medidor(60, 56, 150, 14, self.ehp / e["hp"], VERDE)
        texto("SEG", 20, 80, GRIS, FP)
        medidor(60, 82, 150, 14, self.seg / 100, CIAN, (0, 50, 60))
        texto(f"AMENAZA {self.idx + 1}/{len(ENEMIGOS)}", 680, 28, GRIS, FP, True)
        texto("SOUL.EXE  LV 1", 40, 455, BLANCO, FP)
        texto("HP", 300, 455, BLANCO, FP)
        medidor(335, 455, self.maxhp * 3, 20, self.hp / self.maxhp, AMARILLO, ROJO)
        texto(f"{self.hp}/{self.maxhp}", 345 + self.maxhp * 3, 455, BLANCO, FP)

    def dibujar(self):
        screen.fill((0, 0, 0))
        if self.estado == "titulo":
            return self.pantalla_titulo()
        if self.estado == "fin":
            return self.pantalla_fin()
        r, s = self.rect, self.estado
        if s == "mensaje" and self.quien:  # escena de historia
            if self.quien != "NARRADOR":
                color, simbolo = CAST[self.quien]
                monitor(400, 135 + int(math.sin(pygame.time.get_ticks() / 400) * 6), color, simbolo, BLANCO)
                texto(self.quien, r.left + 22, r.top + 12, color, FP)
            self.escribir(0 if self.quien == "NARRADOR" else 26)
            pygame.draw.rect(screen, BLANCO, r, 4)
            return self.indicador()
        self.enemigo()
        self.hud()
        if s in ("menu", "mensaje"):
            self.escribir()
        elif s == "barra":
            texto("Pulsa Z cuando el cursor esté en la zona amarilla", r.centerx, r.top + 30, AMARILLO, FP, True)
            pygame.draw.rect(screen, (60, 60, 60), (100, 330, 600, 50))
            pygame.draw.rect(screen, VERDE, (250, 330, 300, 50))
            pygame.draw.rect(screen, AMARILLO, (370, 330, 60, 50))
            pygame.draw.rect(screen, BLANCO, (int(self.cx) - 3, 318, 6, 74))
        elif s == "actuar":
            qs = self.e["preguntas"]
            preg, ops = qs[self.qi % len(qs)][:2]
            y = r.top + 14
            for linea in textwrap.wrap(preg, 60):
                texto(linea, r.left + 22, y, AMARILLO, FP)
                y += 22
            for i, o in enumerate(ops):
                texto(o, r.left + 62, y + 8 + i * 28)
                if i == self.sub:
                    corazon(r.left + 40, y + 20 + i * 28)
        elif s == "objeto":
            for i, (nombre, cura, cant) in enumerate(self.items):
                texto(f"{nombre} x{cant} (+{cura} HP)", r.left + 62, r.top + 20 + i * 32)
                if i == self.sub:
                    corazon(r.left + 40, r.top + 32 + i * 32)
        else:  # esquivar
            screen.set_clip(r)
            for b in self.bullets:
                g = glifo(b.ch, self.e["color"])
                screen.blit(g, (int(b.x - g.get_width() / 2), int(b.y - g.get_height() / 2)))
            screen.set_clip(None)
            if self.inv <= 0 or int(self.inv * 12) % 2 == 0:
                corazon(self.px, self.py)
            if self.t < 2.2:  # bocadillo del enemigo
                pygame.draw.rect(screen, BLANCO, (520, 70, 250, 80), border_radius=10)
                for i, linea in enumerate(textwrap.wrap(self.frase, 22)):
                    texto(linea, 532, 80 + i * 22, (0, 0, 0), FP)
        pygame.draw.rect(screen, BLANCO, r, 4)
        for i, nombre in enumerate(("ATACAR", "ACTUAR", "OBJETO", "PERDONAR")):
            x = 40 + i * 185
            col = AMARILLO if i == self.sel and s in ("menu", "barra", "actuar", "objeto") else NARANJA
            pygame.draw.rect(screen, col, (x, 500, 170, 52), 3)
            texto(nombre, x + 100, 526, col, F, True)
        if s == "menu":
            corazon(64 + self.sel * 185, 526)
        self.indicador()

    def pantalla_titulo(self):
        texto("SOUL.EXE", 400, 150, ROJO, FG, True)
        texto("Un juego de ciberseguridad inspirado en Undertale", 400, 225, BLANCO, FP, True)
        texto("Salva la ciudad digital de PIXELIA", 400, 252, GRIS, FP, True)
        corazon(400, 320, ROJO, 1.6)
        texto("Flechas/WASD: mover   Z/Enter: aceptar   X: volver   Esc: salir", 400, 400, GRIS, FP, True)
        texto("Pulsa Z para empezar", 400, 470, AMARILLO, F, True)

    def pantalla_fin(self):
        titulo, color, lineas = FINALES[self.fin]
        texto(titulo, 400, 120, color, FG, True)
        if self.fin != "derrota":
            lineas = lineas + ["", "Recuerda: duda de los enlaces, no instales software pirata,",
                               "usa claves largas con verificación en dos pasos", "y mantén copias de seguridad."]
        for i, linea in enumerate(lineas):
            texto(linea, 400, 230 + i * 30, BLANCO, FP, True)
        accion = "reintentar el capítulo" if self.fin == "derrota" else "jugar de nuevo"
        texto("Pulsa Z para " + accion, 400, 500, AMARILLO, F, True)
