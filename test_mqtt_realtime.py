#!/usr/bin/env python3
"""
Test MQTT real-time data publishing for dashboard
"""

import os
import sys
import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

MQTT_BROKER = 'broker.hivemq.com'
MQTT_PORT = 8883
MQTT_TOPIC = 'xiao/dashboard'

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print('[CONNECT] Connected to HiveMQ broker')
    else:
        print(f'[ERROR] Connection failed: {rc}')

def on_publish(client, userdata, mid, reason_code_list, properties):
    print(f'[PUBLISH] Message published')

print("=" * 70)
print("MQTT REAL-TIME TEST - Publishing to Dashboard")
print("=" * 70)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='test-publisher')
client.on_connect = on_connect
client.on_publish = on_publish

try:
    print(f"\nConnecting to {MQTT_BROKER}:{MQTT_PORT}...")
    client.tls_set()
    client.tls_insecure = True
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_start()
    
    time.sleep(2)
    
    print(f"Sending test data to topic: {MQTT_TOPIC}\n")
    
    # Send 5 messages with incrementing PM2.5
    for i in range(5):
        pm25_value = 28.3 + i * 2.5
        temp_value = 22.5 + i * 0.5
        
        data = {
            'i': 'xiao_001',
            'e': [temp_value, 45.3, 1013.25, 2.5, 750.0, 125.4, 45.2, 65.3],
            'pm': [pm25_value * 0.4, pm25_value, pm25_value * 1.2, pm25_value * 1.5, pm25_value * 1.8],
            'g': [51.5074, -0.1278, 45.2, 0.0],
            't': datetime.now().isoformat()
        }
        
        client.publish(MQTT_TOPIC, json.dumps(data), qos=1)
        print(f"[MESSAGE {i+1}]")
        print(f"  Device: xiao_001")
        print(f"  PM2.5: {data['pm'][1]:.1f} µg/m³")
        print(f"  Temperature: {data['e'][0]:.1f}°C")
        print(f"  Timestamp: {data['t']}\n")
        
        time.sleep(2)
    
    print("=" * 70)
    print("SUCCESS: All test messages sent!")
    print("=" * 70)
    print("\nExpected dashboard updates:")
    print("  ✓ Console shows: 'MQTT message received on xiao/dashboard'")
    print("  ✓ Console shows: 'Parsed MQTT data: {device_id: xiao_001...}'")
    print("  ✓ Charts update with new PM2.5, temperature values")
    print("  ✓ Last Update time refreshes\n")
    
    time.sleep(1)
    
except Exception as e:
    print(f"[ERROR] {e}")
    
finally:
    client.loop_stop()
    client.disconnect()
    print("[DISCONNECT] MQTT client closed")
