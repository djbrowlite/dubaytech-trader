import pandas as pd
import numpy as np

def calcular_atr(data, period=14):
    data['H-L'] = data['high'] - data['low']
    data['H-PC'] = abs(data['high'] - data['close'].shift(1))
    data['L-PC'] = abs(data['low'] - data['close'].shift(1))
    data['TR'] = data[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    data['ATR'] = data['TR'].rolling(window=period).mean()
    return data['ATR']

def calcular_niveles(precio_entrada, atr, factor_riesgo=1.5, factor_beneficio=2):
    stop_loss = precio_entrada - atr * factor_riesgo
    take_profit = precio_entrada + atr * factor_beneficio
    return stop_loss, take_profit

def calcular_lotaje(riesgo_usd, atr, valor_pip):
    stop_pips = atr
    lotaje = riesgo_usd / (stop_pips * valor_pip)
    return round(lotaje, 2)
