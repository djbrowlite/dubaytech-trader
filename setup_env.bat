@echo off
echo Creando entorno virtual...
python -m venv .venv

echo Activando entorno virtual...
call .venv\Scripts\activate.bat

echo Instalando dependencias...
pip install pandas requests

echo Entorno listo. Puedes ejecutar el bot con: python main.py
pause
