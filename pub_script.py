import json
import time
import ssl
import paho.mqtt.client as mqtt

broker = "fb1f89b92da34734b1ca59ef89f2dbfa.s1.eu.hivemq.cloud"
port = 8883
user = "Daksh"
pw = "Sgn@1234"
topic = "sensor/data"

payloads = [
    {"i":"xiao-cam-01","g":[51.5074,-0.1278,20,0],"pm":[10,20,30,40,50],"e":[25,55,1012,3,500,120,60,40],"t":"2026-05-18T13:00:00Z"},
    {"i":"xiao-cam-02","g":[28.6139,77.2090,210,0],"pm":[12,24,36,48,60],"e":[27,50,1009,4,700,140,70,42],"t":"2026-05-18T13:01:00Z"}
]

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.username_pw_set(user, pw)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        for p in payloads:
            client.publish(topic, json.dumps(p))
            print(f"Published to {p['i']}")
    else:
        print(f"Connection failed: {rc}")

client.on_connect = on_connect
client.connect(broker, port)
client.loop_start()
time.sleep(2)
client.loop_stop()
client.disconnect()
