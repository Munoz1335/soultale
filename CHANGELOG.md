# Historial de versiones

## v2.1 - Código modular
- El juego se divide en módulos (`config`, `historia`, `enemigos`, `patrones`, `juego`, `dibujo`, `sonido`...). Se ejecuta con `py main.py`; `soul.py` queda como atajo.
- Modo demo automático para grabar: `py main.py --demo` (`bot.py`).
- Pruebas automáticas en `tests/` (preguntas, enemigos, historia, patrones y recorrido completo del juego).
- Scripts de ayuda: `verificar_entorno.py` y `generar_preguntas_md.py`.
- Documentación nueva: `docs/arquitectura.md`.

## v2.0 - Historia
- Prólogo con narrador y diálogos con FIRU entre capítulos.
- 4 capítulos más un jefe final (ZERO), con 16 preguntas de ciberseguridad.
- Nuevo enemigo: RANSOMWARE (tema: copias de seguridad).
- Puntos de control: curan al jugador y entregan un Antivirus.
- 3 finales: pacifista, neutral y agresivo.
- Globos de texto de los enemigos durante los ataques.

## v1.5 - Versión web
- `index.html`: versión del juego para navegador, con demo automática y modo «Jugar yo» con botones táctiles.
- Publicación en Vercel.

## v1.0 - Primera versión
- Combate por turnos con ATACAR, ACTUAR, OBJETO y PERDONAR.
- Fase de esquivar con el corazón y tres enemigos: PHISHER, TROYANO y FUERZA BRUTA.
