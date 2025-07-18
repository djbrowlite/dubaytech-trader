import requests
import json

# Cargar configuración
with open("config.json") as f:
    config = json.load(f)

OANDA_URL = "https://api-fxpractice.oanda.com/v3"
HEADERS = {
    "Authorization": f"Bearer {config['oanda_token']}",
    "Content-Type": "application/json"
}
ACCOUNT_ID = config["account_id"]

def ejecutar_trade_oanda(symbol, units, stop_loss, take_profit):
    order_data = {
        "order": {
            "instrument": symbol,
            "units": str(units),
            "type": "MARKET",
            "positionFill": "DEFAULT",
            "takeProfitOnFill": {
                "price": f"{take_profit:.5f}"
            },
            "stopLossOnFill": {
                "price": f"{stop_loss:.5f}"
            }
        }
    }

    response = requests.post(
        f"{OANDA_URL}/accounts/{ACCOUNT_ID}/orders",
        headers=HEADERS,
        json=order_data
    )

    if response.status_code == 201:
        print("✅ Orden ejecutada correctamente")
    else:
        print(f"❌ Error al ejecutar orden: {response.text}")
