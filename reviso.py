import paho.mqtt.client as mqtt

# Configuración
BROKER_URL = "crossover.proxy.rlwy.net"
BROKER_PORT = 57689
TOPIC = "ard/12"

# Función cuando se conecta
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT")
        client.subscribe(TOPIC)
    else:
        print("Error de conexión, código:", rc)

# Función cuando llega un mensaje
def on_message(client, userdata, msg):
    print(f"Mensaje recibido en '{msg.topic}': {msg.payload.decode()}")

# Crear cliente y asignar funciones
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Conectar y mantener loop
client.connect(BROKER_URL, BROKER_PORT, 60)
client.loop_forever()
