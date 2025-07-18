import tkinter as tk
from tkinter import ttk
from threading import Thread
import time
from risk_manager import calcular_atr, calcular_niveles, calcular_lotaje
from oanda_api import ejecutar_trade_oanda
from discord_alerts import enviar_alerta_discord
from trade_manager import registrar_operacion, cerrar_operaciones
import pandas as pd

class TradingBotGUI:
    def __init__(self, master):
        self.master = master
        master.title("DubayTech Volatility Trader")
        master.geometry("600x500")

        # Pestañas
        self.tabs = ttk.Notebook(master)
        self.control_tab = ttk.Frame(self.tabs)
        self.operaciones_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.control_tab, text="Panel de Control")
        self.tabs.add(self.operaciones_tab, text="Operaciones")
        self.tabs.pack(expand=1, fill="both")

        # Logo
        self.logo = tk.PhotoImage(file="assets/logo.png")
        tk.Label(self.control_tab, image=self.logo).pack()

        # Símbolo
        tk.Label(self.control_tab, text="Símbolo:").pack()
        self.symbol_var = tk.StringVar()
        symbols = ["US30", "SPX500", "NAS100", "GER30", "FRA40", "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF", "NZDUSD", "USDCAD"]
        self.symbol_menu = tk.OptionMenu(self.control_tab, self.symbol_var, *symbols)
        self.symbol_menu.pack()

        # Riesgo
        tk.Label(self.control_tab, text="Riesgo ($):").pack()
        self.riesgo_entry = tk.Entry(self.control_tab)
        self.riesgo_entry.pack()

        # Modo
        self.modo_demo = tk.BooleanVar()
        tk.Checkbutton(self.control_tab, text="Modo Demo", variable=self.modo_demo).pack()

        # Activar/Desactivar
        self.running = False
        self.toggle_button = tk.Button(self.control_tab, text="Activar Bot", command=self.toggle_bot)
        self.toggle_button.pack()

        # Estado
        self.status_label = tk.Label(self.control_tab, text="Estado: Inactivo")
        self.status_label.pack()

        # Tabla de operaciones cerradas
        self.tree = ttk.Treeview(self.operaciones_tab, columns=("Fecha", "Símbolo", "Entrada", "SL", "TP", "Lotaje", "Modo", "Resultado"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        self.actualizar_historial()

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
            data = self.obtener_datos_ohlc(symbol)
            atr = calcular_atr(data)[-1]
            precio = data['close'].iloc[-1]
            sl, tp = calcular_niveles(precio, atr)
            lotaje = calcular_lotaje(riesgo, atr, valor_pip=1)

            if modo == "real":
                ejecutar_trade_oanda(symbol, lotaje, sl, tp)
            registrar_operacion(symbol, precio, sl, tp, lotaje, modo)
            enviar_alerta_discord(f"{modo.upper()} Trade ejecutado: {symbol} | SL: {sl:.2f} | TP: {tp:.2f} | Lotaje: {lotaje}")

            time.sleep(300)  # Ejecuta cada 5 minutos
            cerrar_operaciones()
            self.actualizar_historial()

    def obtener_datos_ohlc(self, symbol):
        # Simulación de datos OHLC para pruebas
        data = pd.DataFrame({
            "open": [100 + i for i in range(30)],
            "high": [102 + i for i in range(30)],
            "low": [98 + i for i in range(30)],
            "close": [101 + i for i in range(30)]
        })
        return data

    def actualizar_historial(self):
        try:
            df = pd.read_csv("logs/operaciones.csv")
            self.tree.delete(*self.tree.get_children())
            for _, row in df.iterrows():
                self.tree.insert("", "end", values=tuple(row))
        except Exception as e:
            print(f"Error al cargar historial: {e}")
