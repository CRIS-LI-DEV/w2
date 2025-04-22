import json
import time
import paho.mqtt.client as mqtt

# Configuración
BROKER_URL = "crossover.proxy.rlwy.net"
BROKER_PORT = 57689
TOPIC = "ard/12"
INTERVALO_SEGUNDOS = 3  # Intervalo entre publicaciones

# Crear cliente MQTT
client = mqtt.Client()

# Función callback para cuando el cliente se conecta
def on_connect(client, userdata, flags, rc):
    print(f"Conectado al broker con código de resultado: {rc}")
    if rc == 0:
        print(f"Listo para publicar en el tópico {TOPIC}")

# Conectar al broker MQTT
client.on_connect = on_connect

# Publicar el mensaje JSON
def publicar_mensaje():
    mensaje_falso = {
        "a11": 1,
        "a12": 0,
        "s09": 1,
        "s10": 0,
        "s11": 0,
        "s12": 500,
        "s13": 600,
        "s14": 700
    }
    payload = json.dumps(mensaje_falso)
    print(f"Publicando mensaje: {payload}")
    result = client.publish(TOPIC, payload)
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print("Mensaje publicado con éxito.")
    else:
        print(f"Error al publicar el mensaje: {result.rc}")

def main():
    try:
        # Conectar al broker
        client.connect(BROKER_URL, BROKER_PORT, 60)
        client.loop_start()

        while True:
            # Publicar el mensaje en un bucle infinito
            publicar_mensaje()
            # Esperar un intervalo antes de publicar nuevamente
            time.sleep(INTERVALO_SEGUNDOS)

    except Exception as e:
        print(f"Error al conectar o publicar: {e}")

if __name__ == "__main__":
    main()
