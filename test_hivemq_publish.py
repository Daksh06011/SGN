import paho.mqtt.client as mqtt
import json
import ssl
import time
from datetime import datetime, timezone

broker = "fb1f89b92da34734b1ca59ef89f2dbfa.s1.eu.hivemq.cloud"
port = 8883
topic = "sensor/data"

payload = {
  "site": "xiao-cam-01",
  "mac": "90:70:69:12:B9:CC",
  "ts": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
  "ip": "192.168.31.221",
  "rssi": -67,
  "lat": 0,
  "lon": 0,
  "sound": 0,
  "no2": 0,
  "voc": 0,
  "tsi": "ok",
  "tsi_serial": "81432008054",
  "tsi_pm1": 7,
  "tsi_pm25": 7,
  "tsi_pm4": 7,
  "tsi_pm10": 7,
  "tsi_temp": 30.200000762939453,
  "tsi_rh": 72
}

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.publish(topic, json.dumps(payload))
    print(f"Published exact payload to {topic}")

client = mqtt.Client()
client.username_pw_set("Daksh", "Sgn@1234")
client.tls_set(tls_version=ssl.PROTOCOL_TLS)
client.on_connect = on_connect

client.connect(broker, port, 60)
client.loop_start()

time.sleep(3) # Wait for publish to finish
client.loop_stop()
client.disconnect()
print("Done")
