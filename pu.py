import json
import time
import requests
import paho.mqtt.client as mqtt

# Configuración
BROKER_URL = "crossover.proxy.rlwy.net"
BROKER_PORT = 57689
DATA_URL = "https://viz1-production.up.railway.app/br-out/"
TOPIC = "ard/12"
ID_SOLICITADO = 12
INTERVALO_SEGUNDOS = 10

# Crear cliente MQTT
client = mqtt.Client()

# Función callback para cuando el cliente se conecta
def on_connect(client, userdata, flags, rc):
    print(f"Conectado al broker con código de resultado: {rc}")
    if rc == 0:
        client.subscribe(TOPIC)  # Subscribirse si se necesita

# Función callback para cuando el cliente publica un mensaje
def on_publish(client, userdata, mid):
    print(f"Mensaje publicado con ID: {mid}")

# Función para enviar el mensaje completo
def enviar_completo(data):
    payload = json.dumps(data)
    print(f"Enviando a tópico {TOPIC}: {payload}")
    result = client.publish(TOPIC, payload)
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print("Mensaje publicado con éxito.")
    else:
        print(f"Error al publicar el mensaje: {result.rc}")

def main():
    try:
        client.on_connect = on_connect
        client.on_publish = on_publish
        
        client.connect(BROKER_URL, BROKER_PORT, 60)
        client.loop_start()

        while True:
            try:
                headers = {'Content-Type': 'application/json'}
                response = requests.post(DATA_URL, headers=headers, json={"id": ID_SOLICITADO})
                
                if response.status_code == 201:
                    data = response.json()
                    print("Respuesta de la API completa:", json.dumps(data, indent=2))
                    
                    enviar_completo(data)  # Enviar SIEMPRE el JSON completo
                else:
                    print(f"Error al obtener datos (status {response.status_code}): {response.text}")
            
            except Exception as e:
                print(f"Error durante la solicitud/post: {e}")
            
            time.sleep(INTERVALO_SEGUNDOS)
    
    except Exception as e:
        print(f"Error de conexión MQTT: {e}")
    
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
