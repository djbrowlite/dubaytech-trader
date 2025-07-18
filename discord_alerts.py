import requests
import json

# Cargar configuración
with open("config.json") as f:
    config = json.load(f)

WEBHOOK_URL = config["discord_webhook"]

def enviar_alerta_discord(mensaje):
    payload = {"content": mensaje}
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("✅ Alerta enviada a Discord")
        else:
            print(f"❌ Error al enviar alerta: {response.text}")
    except Exception as e:
        print(f"❌ Excepción al enviar alerta: {e}")
