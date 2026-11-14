# SOUL.EXE

Juego de ciberseguridad con combates por turnos. Eres un pequeño antivirus con forma de corazón que debe salvar la ciudad digital de **PIXELIA**, tomada por **ZERO**. Para lograrlo tienes que esquivar ataques y responder preguntas de seguridad informática: cada amenaza puede destruirse o convencerse, y eso cambia el final.

## Estructura del repositorio

```text
soul.exe/
├── main.py                     Punto de entrada del juego
├── soul.py                     Atajo: también funciona `py soul.py`
├── config.py                   Constantes (colores, tamaños, vida)
├── historia.py                 Prólogo, finales y textos
├── enemigos.py                 Enemigos, preguntas y personajes
├── balas.py                    Clase Bala
├── patrones.py                 Patrones de ataque
├── controles.py                Teclas y movimiento
├── motor.py                    Ventana, reloj y fuentes de pygame
├── sonido.py                   Pitidos generados por código
├── dibujo.py                   Funciones de dibujo
├── juego.py                    Lógica del combate y las escenas
├── bot.py                      Jugador automático para la demo
├── index.html                  Versión web (se publica en Vercel)
├── requirements.txt            Dependencias
├── ejecutar_windows.bat        Instala todo y abre el juego (Windows)
├── ejecutar_demo_windows.bat   Abre la demo automática (Windows)
├── CHANGELOG.md                Historial de versiones
├── .gitignore                  Archivos que Git ignora
├── scripts/
│   ├── verificar_entorno.py        Comprueba Python y pygame-ce
│   └── generar_preguntas_md.py     Regenera docs/preguntas.md
├── tests/
│   ├── test_preguntas.py
│   ├── test_enemigos.py
│   ├── test_historia.py
│   ├── test_patrones.py
│   └── test_juego.py
└── docs/
    ├── arquitectura.md         Módulos y cómo agregar un enemigo
    ├── historia.md             Historia, personajes y finales
    ├── reglas.md               Reglas y mecánicas detalladas
    ├── preguntas.md            Banco de preguntas con respuestas
    └── SOUL_EXE_guia.pdf       Guía completa: mecánicas, GitHub, Vercel y OBS
```

## Documentación

- [Arquitectura del código](docs/arquitectura.md)
- [Historia y personajes](docs/historia.md)
- [Reglas y mecánicas](docs/reglas.md)
- [Banco de preguntas](docs/preguntas.md)
- [Guía completa en PDF](docs/SOUL_EXE_guia.pdf)
- [Historial de versiones](CHANGELOG.md)

## Cómo ejecutar la versión de Python

1. Instala [Python](https://www.python.org/downloads/).
2. Instala las dependencias: `py -m pip install -r requirements.txt`
3. Ejecuta el juego: `py main.py`

En Windows también puedes hacer doble clic en `ejecutar_windows.bat`, que instala todo y abre el juego.

| Comando | Para qué sirve |
|---|---|
| `py main.py --demo` | Demo automática: el juego se juega solo (ideal para grabar con OBS) |
| `py scripts/verificar_entorno.py` | Comprueba que Python y pygame-ce están instalados |
| `py -m unittest discover -s tests -v` | Ejecuta las pruebas automáticas |
| `py scripts/generar_preguntas_md.py` | Regenera `docs/preguntas.md` desde el código |

La versión web no necesita instalación: basta con abrir `index.html` en un navegador.

## Controles

| Tecla | Función |
|---|---|
| Flechas o WASD | Mover el corazón y navegar por los menús |
| Z o Enter | Aceptar y avanzar el texto |
| X | Volver atrás |
| Esc | Salir (solo en la versión de Python) |

## Historia

Una noche toda la red de Pixelia se apagó y los programas guardianes desaparecieron, todos menos uno: tú, **SOUL.EXE**. **FIRU**, el último firewall, te guía por cuatro zonas hasta el Centro de Control, donde espera **ZERO**.

ZERO fue un guardián creado para avisar de los fallos de seguridad de Pixelia. Avisó mil veces y nadie lo escuchó, así que decidió enseñarles por las malas. Al final tú decides si lo destruyes o lo convences.

## Reglas

Cada turno tiene dos partes: eliges una acción y después el enemigo ataca durante 7 segundos mientras esquivas.

| Acción | Qué hace |
|---|---|
| **ATACAR** | Una barra con un cursor: pulsa Z en la zona amarilla. Cuanto más cerca del centro, más daño (de 2 a 30). |
| **ACTUAR** | Pregunta de ciberseguridad con 3 respuestas. Acertar sube la barra SEG un 50% (34% contra ZERO). Fallar enoja al enemigo. |
| **OBJETO** | Antivirus (+12 HP, empiezas con 2) y Copia de seguridad (+25 HP, empiezas con 1). |
| **PERDONAR** | Solo funciona con SEG al 100%: neutralizas la amenaza sin violencia. Si no, pierdes el turno. |

- Empiezas con **30 HP**. Cada golpe quita 4 HP y da 1 segundo de invulnerabilidad.
- Cada respuesta incorrecta sube el **enojo** del enemigo (máximo 3): sus ataques son un 20% más rápidos y cada golpe quita 1 HP extra.
- Al terminar cada capítulo, excepto el final, recuperas toda la vida y ganas 1 Antivirus (punto de control).
- Si pierdes, puedes reintentar el capítulo con la vida completa.

## Capítulos

| Capítulo | Enemigo | Tema | HP | Ataque |
|---|---|---|---|---|
| 1. El buzón | PHISHER | Phishing y dominios falsos | 40 | Lluvia de `@` |
| 2. La zona de descargas | TROYANO | Software pirata, actualizaciones, USB | 50 | Disparos de `0` y `1` |
| 3. La bóveda de claves | FUERZA BRUTA | Contraseñas y verificación en dos pasos | 60 | Muro de `*` con un hueco |
| 4. Los archivos secuestrados | RANSOMWARE | Copias de seguridad y adjuntos peligrosos | 70 | Monedas `$` laterales |
| Final: el centro de control | ZERO | Wi-Fi público, códigos de verificación | 90 | Mezcla de todos |

## Finales

- **Pacifista:** no destruyes a ningún enemigo y perdonas a ZERO. ZERO se une a FIRU como guardián.
- **Neutral:** destruyes a algún enemigo, pero perdonas a ZERO.
- **Agresivo:** destruyes a ZERO. La red vuelve a encenderse, pero nadie aprendió nada.
