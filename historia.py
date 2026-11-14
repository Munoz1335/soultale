"""Textos de la historia: prólogo, finales y pantallas finales (sin pygame)."""
from config import AMARILLO, ROJO, VERDE

PROLOGO = [
    ("NARRADOR", "* Hace tiempo, la ciudad digital de PIXELIA vivía en paz. Cada casa, banco y escuela estaba conectada a una sola red."),
    ("NARRADOR", "* Hasta que una noche todo se apagó. Los programas guardianes desaparecieron... todos menos uno."),
    ("NARRADOR", "* Tú. Un pequeño antivirus con forma de corazón: SOUL.EXE. Acabas de despertar."),
    ("FIRU", "¡Por fin despiertas! Soy FIRU, el último firewall de Pixelia. Alguien llamado ZERO tomó el control de la red."),
    ("FIRU", "Para llegar hasta él debes cruzar cuatro zonas. Cada amenaza usa un truco distinto... y todas pueden aprender."),
    ("FIRU", "No siempre hay que destruir lo que nos ataca. A veces basta con entenderlo. Usa ACTUAR con cabeza."),
]
FIN_PACIFISTA = [
    ("ZERO", "...Nadie me había escuchado así. Tenías razón: mi trabajo era avisar, no vengarme."),
    ("FIRU", "¡Zero! ¡Sabía que seguías ahí, amigo!"),
    ("ZERO", "Déjame arreglarlo. Conozco cada grieta de esta red... y sé cómo cerrarlas."),
    ("NARRADOR", "* ZERO devuelve el control y se une a FIRU como guardián. Las luces de Pixelia vuelven a encenderse."),
    ("NARRADOR", "* Aprendiste que la mejor defensa es entender, avisar y cuidar. Gracias por jugar."),
]
FIN_NEUTRAL = [
    ("ZERO", "Me perdonas... pero dejaste amenazas borradas por el camino. Yo también pude haber sido una de ellas."),
    ("FIRU", "La red se salvó, pero hay cosas que no volverán. Aprende de eso."),
    ("NARRADOR", "* ZERO se queda como vigilante, a prueba. Pixelia vuelve a encenderse, con cicatrices."),
]
FIN_AGRESIVA = [
    ("ZERO", "Entonces... así termina. Nadie sabrá nunca por qué lo hice."),
    ("FIRU", "No quería que acabara así..."),
    ("NARRADOR", "* La red vuelve a encenderse. Pero sin entender qué pasó, nadie cambia sus claves ni actualiza sus equipos."),
    ("NARRADOR", "* Y en alguna parte, otro atacante ya está despertando."),
]
FINALES = {
    "pacifista": ("RUTA PACIFISTA", VERDE, ["Defendiste la red sin destruir nada.", "ZERO ahora protege Pixelia contigo."]),
    "neutral": ("RUTA NEUTRAL", AMARILLO, ["Salvaste Pixelia, pero borraste amenazas sin entenderlas."]),
    "agresiva": ("RUTA AGRESIVA", ROJO, ["Ganaste por la fuerza... y nadie aprendió nada."]),
    "derrota": ("CONEXIÓN PERDIDA", ROJO, ["Los atacantes ganaron esta vez.", "No te rindas... ¡Reinicia el sistema!"]),
}
