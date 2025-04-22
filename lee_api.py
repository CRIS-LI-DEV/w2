import json
import time
import requests
import paho.mqtt.client as mqtt


DATA_URL = "https://viz1-production.up.railway.app/br-out/"

datos = {
    'id':12
}


response = requests.post(DATA_URL, json=datos)

# Verificar el resultado
if response.status_code == 200:
    print('POST enviado correctamente:', response.json())
else:
    print('Error al enviar el POST:', response.status_code,  response.json())