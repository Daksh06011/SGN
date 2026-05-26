#!/usr/bin/env python3
"""Send test TSI data to MQTT broker"""

import paho.mqtt.client as mqtt
import json
import time
import sys
import io

# Fix Unicode/emoji output in Windows PowerShell
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# MQTT Configuration
MQTT_BROKER = "461dec45331a4366882762ab7221c726.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "hivemq.webclient.1765452496255"
MQTT_PASSWORD = "24csnE%<MLVSQ#6d9!zb"
MQTT_TOPIC = "sensor/data"

# Test data from user
test_data = {
    "site": "xiao-cam-01",
    "mac": "90:70:69:12:B9:CC",
    "ts": "2026-05-15 14:06:00",
    "ip": "192.168.31.221",
    "rssi": -67,
    "lat": 51.5074,
    "lon": -0.1278,
    "sound": 0,
    "no2": 0,
    "voc": 0,
    "tsi": "ok",
    "tsi_serial": "81432008054",
    "tsi_pm1": 7,
    "tsi_pm25": 7,
    "tsi_pm4": 7,
    "tsi_pm10": 7,
    "tsi_temp": 30.2,
    "tsi_rh": 72
}

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Connected to MQTT broker!")
    else:
        print(f"❌ Connection failed with code: {rc}")

def on_publish(client, userdata, mid, reason_code_list, properties):
    print(f"✅ Data published successfully!")

print("=" * 80)
print("📡 SENDING TEST TSI DATA TO MQTT")
print("=" * 80)
print(f"🖥️  Broker:  {MQTT_BROKER}:{MQTT_PORT}")
print(f"📝 Topic:   {MQTT_TOPIC}")
print(f"📊 Data:    {json.dumps(test_data, indent=2)}")
print()

# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="test-tsi-publisher")
client.on_connect = on_connect
client.on_publish = on_publish

try:
    # Set TLS
    client.tls_set()
    client.tls_insecure = True
    
    # Connect to broker
    print("🔗 Connecting to broker...")
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_start()
    
    # Wait for connection
    time.sleep(2)
    
    # Send the test data
    print("\n" + "=" * 80)
    print("📊 SENDING TEST DATA")
    print("=" * 80)
    print()
    
    payload = json.dumps(test_data)
    info = client.publish(MQTT_TOPIC, payload, qos=1)
    
    # Wait a bit for publish to complete
    time.sleep(2)
    
    # Send it a few more times to populate the chart
    print("\n📊 Sending data multiple times to populate chart history...")
    for i in range(3):
        time.sleep(1)
        client.publish(MQTT_TOPIC, payload, qos=1)
        print(f"   Sent {i+2}/4")
    
    print("\n✨ Data sent successfully!")
    print("\n💡 Refresh the dashboard to see the data!")
    
    client.loop_stop()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    client.disconnect()
