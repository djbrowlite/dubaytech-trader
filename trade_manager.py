import time
import csv
from datetime import datetime

operaciones_activas = []

def registrar_operacion(symbol, precio_entrada, sl, tp, lotaje, modo):
    operacion = {
        "symbol": symbol,
        "precio_entrada": precio_entrada,
        "sl": sl,
        "tp": tp,
        "lotaje": lotaje,
        "modo": modo,
        "inicio": time.time()
    }
    operaciones_activas.append(operacion)

def cerrar_operaciones():
    cerradas = []
    ahora = time.time()
    for op in operaciones_activas[:]:
        if ahora - op["inicio"] >= 300:  # 5 minutos
            resultado = simular_resultado(op)
            guardar_en_historial(op, resultado)
            operaciones_activas.remove(op)
            cerradas.append(op)
    return cerradas

def simular_resultado(op):
    # Simulación simple: ganancia si TP > entrada, pérdida si SL < entrada
    if op["tp"] > op["precio_entrada"]:
        return "Ganancia"
    else:
        return "Pérdida"

def guardar_en_historial(op, resultado):
    with open("logs/operaciones.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            op["symbol"],
            op["precio_entrada"],
            op["sl"],
            op["tp"],
            op["lotaje"],
            op["modo"],
            resultado
        ])
