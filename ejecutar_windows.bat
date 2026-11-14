@echo off
echo ==================================
echo   SOUL.EXE - Instalar y jugar
echo ==================================
echo.
echo Instalando dependencias (pygame-ce)...
py -m pip install -r requirements.txt
echo.
echo Iniciando el juego...
py main.py
pause
