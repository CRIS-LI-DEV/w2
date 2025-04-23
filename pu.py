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
        client.subscribe(TOPIC)  # Si es necesario, subscribirse a un topic.

# Función callback para cuando el cliente publica un mensaje
def on_publish(client, userdata, mid):
    print(f"Mensaje publicado con ID: {mid}")

# Función para enviar el mensaje completo
def enviar_completo(data):
    # Aquí simplemente enviamos todo el JSON recibido
    payload = json.dumps(data)
    print(f"Enviando a tópico {TOPIC}: {payload}")
    result = client.publish(TOPIC, payload)
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print("Mensaje publicado con éxito.")
    else:
        print(f"Error al publicar el mensaje: {result.rc}")

def main():
    try:
        # Establecer callbacks
        client.on_connect = on_connect
        client.on_publish = on_publish
        
        # Conectar al broker MQTT
        client.connect(BROKER_URL, BROKER_PORT, 60)
        client.loop_start()

        while True:
            try:
                # Hacer la solicitud POST con {"id": 12}
                headers = {'Content-Type': 'application/json'}
                response = requests.post(DATA_URL, headers=headers, json={"id": ID_SOLICITADO})
                
                if response.status_code == 200:
                    data = response.json()
                    print("Respuesta de la API completa:", json.dumps(data, indent=2))  # Ver los datos completos
                    
                    if data.get("cwc"):  # Verificar si "cwc" es verdadero
                        enviar_completo(data)  # Enviar todo el JSON
                    else:
                        print("No se debe enviar nada. 'cwc' es False.")
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
