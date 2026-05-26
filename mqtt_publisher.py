#!/usr/bin/env python3
"""
MQTT Data Publisher - Send data to MQTT broker
"""

import os
import sys
import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

# Fix Unicode/emoji output in Windows PowerShell
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# MQTT Configuration
MQTT_BROKER = os.getenv('MQTT_BROKER', "broker.hivemq.com")
MQTT_PORT = int(os.getenv('MQTT_PORT', 8883))
MQTT_USE_TLS = os.getenv('MQTT_USE_TLS', 'true').lower() == 'true'
MQTT_TOPIC = os.getenv('MQTT_TOPIC', "xiao/dashboard")

def on_connect(client, userdata, flags, rc, properties=None):
    """Connection callback"""
    if rc == 0:
        print("✅ Connected to MQTT broker!")
    else:
        print(f"❌ Connection failed with code: {rc}")

def on_publish(client, userdata, mid, reason_code_list, properties):
    """Publish callback"""
    print(f"✅ Message published successfully (ID: {mid})")

def send_sensor_data():
    """Send sensor data to MQTT broker"""
    
    print("=" * 80)
    print("📡 MQTT DATA PUBLISHER")
    print("=" * 80)
    print(f"🖥️  Broker:  {MQTT_BROKER}:{MQTT_PORT}")
    print(f"📝 Topic:   {MQTT_TOPIC}")
    print(f"🔐 TLS:     {MQTT_USE_TLS}")
    print()
    
    # Create MQTT client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="python-publisher")
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    try:
        # Connect to broker
        print("🔗 Connecting to broker...")
        
        # Set TLS if needed (for public brokers)
        if MQTT_USE_TLS:
            client.tls_set()
            client.tls_insecure = True  # For testing only
            print("   🔒 Using TLS connection")
        
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        client.loop_start()
        
        # Wait for connection
        time.sleep(2)
        
        # Sample data to send
        print("\n" + "=" * 80)
        print("📊 SENDING SAMPLE DATA")
        print("=" * 80)
        print()
        
        # ========== FORMAT 1: COMPACT FORMAT (Recommended) ==========
        print("1️⃣  COMPACT FORMAT - Latest recommended format")
        print("-" * 80)
        
        compact_data = {
            "i": "xiao_001",          # Device ID (can also use "deviceid")
            "e": [                     # Environmental array [temp, humidity, pressure, uv, lux, voc, no2, noise]
                22.5,                  # Temperature (°C)
                45.3,                  # Humidity (%)
                1013.25,               # Pressure (hPa)
                2.5,                   # UV Index
                750.0,                 # Lux (light level)
                125.4,                 # VOC (ppb)
                45.2,                  # NO2 (ppb)
                65.3                   # Noise (dB)
            ],
            "pm": [                    # Particulate Matter array [pm1, pm2.5, pm4, pm10, tsp]
                12.5,                  # PM1 (µg/m³)
                28.3,                  # PM2.5 (µg/m³)
                35.1,                  # PM4 (µg/m³)
                42.8,                  # PM10 (µg/m³)
                50.0                   # TSP (µg/m³)
            ],
            "g": [                     # GPS array [latitude, longitude, altitude, speed]
                51.5074,               # Latitude
                -0.1278,               # Longitude
                45.2,                  # Altitude (meters)
                0.0                    # Speed (km/h)
            ],
            "t": datetime.now().isoformat()  # Timestamp
        }
        
        print("📤 Publishing compact format data...")
        print(f"   Data: {json.dumps(compact_data, indent=2)}")
        
        client.publish(MQTT_TOPIC, json.dumps(compact_data), qos=1)
        time.sleep(1)
        
        # ========== FORMAT 2: EXTENDED FORMAT ==========
        print("\n2️⃣  EXTENDED FORMAT - Traditional detailed format")
        print("-" * 80)
        
        extended_data = {
            "deviceid": "xiao_001",
            "Temperature_C": 23.1,
            "Humidity_%": 42.8,
            "Pressure_hPa": 1012.95,
            "UV_Index": 2.3,
            "Lux": 720.0,
            "VOC_ppb": 132.1,
            "NO2_ppb": 48.7,
            "Noise_dB": 67.2,
            "PM_data": {
                "PM1": 15.2,
                "PM2_5": 32.8,
                "PM4": 40.5,
                "PM10": 48.9,
                "TSP": 55.3
            },
            "GPS": {
                "Latitude": 51.5074,
                "Longitude": -0.1278,
                "Altitude_m": 45.2,
                "Speed_kmh": 0.0
            }
        }
        
        print("📤 Publishing extended format data...")
        print(f"   Data: {json.dumps(extended_data, indent=2)}")
        
        client.publish(MQTT_TOPIC, json.dumps(extended_data), qos=1)
        time.sleep(1)
        
        # ========== FORMAT 3: SIMPLE FORMAT ==========
        print("\n3️⃣  SIMPLE FORMAT - Minimal sensor-only data")
        print("-" * 80)
        
        simple_data = {
            "deviceid": "xiao_001",
            "pm1": 18.9,
            "pm2_5": 38.4,
            "pm4": 45.2,
            "pm10": 52.1,
            "tsp": 58.9
        }
        
        print("📤 Publishing simple format data...")
        print(f"   Data: {json.dumps(simple_data, indent=2)}")
        
        client.publish(MQTT_TOPIC, json.dumps(simple_data), qos=1)
        time.sleep(1)
        
        # ========== CONTINUOUS MODE ==========
        print("\n" + "=" * 80)
        print("4️⃣  CONTINUOUS PUBLISHING MODE")
        print("-" * 80)
        print("Publishing data every 10 seconds (press Ctrl+C to stop)")
        print()
        
        counter = 0
        try:
            while True:
                counter += 1
                
                # Generate random sensor data
                base_pm25 = 30 + random.uniform(-5, 10)
                base_temp = 23 + random.uniform(-2, 2)
                base_humidity = 40 + random.uniform(-5, 5)
                
                data = {
                    "i": "xiao_001",
                    "e": [
                        base_temp,
                        base_humidity,
                        1012 + random.uniform(-2, 2),
                        2.0 + random.uniform(-1, 1),
                        700 + random.uniform(-100, 100),
                        130 + random.uniform(-10, 10),
                        50 + random.uniform(-10, 10),
                        65 + random.uniform(-5, 5)
                    ],
                    "pm": [
                        base_pm25 * 0.3,
                        base_pm25,
                        base_pm25 * 1.2,
                        base_pm25 * 1.5,
                        base_pm25 * 1.8
                    ],
                    "g": [51.5074, -0.1278, 45.2, 0.0],
                    "t": datetime.now().isoformat()
                }
                
                print(f"📤 [{counter}] Publishing data at {data['t']}")
                print(f"    PM2.5: {data['pm'][1]:.1f} µg/m³")
                print(f"    Temp:  {data['e'][0]:.1f}°C")
                print(f"    Humidity: {data['e'][1]:.1f}%")
                
                client.publish(MQTT_TOPIC, json.dumps(data), qos=1)
                time.sleep(10)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Publishing stopped")
        
    except ConnectionRefusedError:
        print(f"❌ Connection refused - is the broker running at {MQTT_BROKER}:{MQTT_PORT}?")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        print("\n✅ Disconnected")

def send_single_message(device_id, pm25, temperature):
    """Send a single message with custom values"""
    
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="python-publisher")
    
    try:
        if MQTT_USE_TLS:
            client.tls_set()
            client.tls_insecure = True
        
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        client.loop_start()
        time.sleep(1)
        
        data = {
            "i": device_id,
            "e": [temperature, 40.0, 1013.0, 2.0, 750.0, 130.0, 50.0, 65.0],
            "pm": [pm25*0.3, pm25, pm25*1.2, pm25*1.5, pm25*1.8],
            "g": [51.5074, -0.1278, 45.2, 0.0],
            "t": datetime.now().isoformat()
        }
        
        client.publish(MQTT_TOPIC, json.dumps(data), qos=1)
        print(f"✅ Sent data: Device={device_id}, PM2.5={pm25} µg/m³, Temp={temperature}°C")
        time.sleep(1)
        
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "custom":
        # Custom mode: python mqtt_publisher.py custom <device_id> <pm25> <temperature>
        device_id = sys.argv[2] if len(sys.argv) > 2 else "xiao_001"
        pm25 = float(sys.argv[3]) if len(sys.argv) > 3 else 35.0
        temp = float(sys.argv[4]) if len(sys.argv) > 4 else 23.0
        send_single_message(device_id, pm25, temp)
    else:
        # Demo mode
        send_sensor_data()
