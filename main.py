import os

# Inicialización de carpeta y archivo de historial
os.makedirs("logs", exist_ok=True)
csv_path = "logs/operaciones.csv"
if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
    with open(csv_path, mode="w", newline="") as file:
        file.write("Fecha,Symbol,Precio Entrada,Stop Loss,Take Profit,Lotaje,Modo,Resultado\n")

import tkinter as tk
from gui import TradingBotGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotGUI(root)
    root.mainloop()
