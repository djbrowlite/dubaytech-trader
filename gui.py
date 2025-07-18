import tkinter as tk
from threading import Thread
from risk_manager import calcular_atr, calcular_niveles, calcular_lotaje
from oanda_api import ejecutar_trade_oanda
from discord_alerts import enviar_alerta_discord
import time

class TradingBotGUI:
    def __init__(self, master):
        self.master = master
        master.title("DubayTech Volatility Trader")
        master.geometry("400x400")

        # Logo
        self.logo = tk.PhotoImage(file="assets/logo.png")
        tk.Label(master, image=self.logo).pack()

        # Símbolo
        tk.Label(master, text="Símbolo:").pack()
        self.symbol_var = tk.StringVar()
        self.symbol_menu = tk.OptionMenu(master, self.symbol_var, "US30", "SPX500", "EURUSD", "GBPUSD")
        self.symbol_menu.pack()

        # Riesgo
        tk.Label(master, text="Riesgo ($):").pack()
        self.riesgo_entry = tk.Entry(master)
        self.riesgo_entry.pack()

        # Modo
        self.modo_demo = tk.BooleanVar()
        tk.Checkbutton(master, text="Modo Demo", variable=self.modo_demo).pack()

        # Activar/Desactivar
        self.running = False
        self.toggle_button = tk.Button(master, text="Activar Bot", command=self.toggle_bot)
        self.toggle_button.pack()

        # Estado
        self.status_label = tk.Label(master, text="Estado: Inactivo")
        self.status_label.pack()

    def toggle_bot(self):
        self.running = not self.running
        self.toggle_button.config(text="Desactivar Bot" if self.running else "Activar Bot")
        self.status_label.config(text="Estado: Activo" if self.running else "Estado: Inactivo")
        if self.running:
            Thread(target=self.run_bot).start()

    def run_bot(self):
        while self.running:
            symbol = self.symbol_var.get()
            riesgo = float(self.riesgo_entry.get())
            modo = "demo" if self.modo_demo.get() else "real"

            # Simulación de datos OHLC
            data = obtener_datos_ohlc(symbol)
            atr = calcular_atr(data)[-1]
            precio = data['close'].iloc[-1]
            sl, tp = calcular_niveles(precio, atr)
            lotaje = calcular_lotaje(riesgo, atr, valor_pip=1)

            if modo == "real":
                ejecutar_trade_oanda(symbol, lotaje, sl, tp)
            enviar_alerta_discord(f"{modo.upper()} Trade ejecutado: {symbol} | SL: {sl:.2f} | TP: {tp:.2f} | Lotaje: {lotaje}")

            time.sleep(300)  # Ejecuta cada 5 minutos
