#!/usr/bin/env python3
"""
MQTTX Helper - Publish test payloads quickly
Usage: python mqttx_helper.py [scenario]
"""

import os
import sys
import json
import time
import paho.mqtt.client as mqtt
from datetime import datetime

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configuration
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC = 'xiao/dashboard'
DEVICE_ID = 'xiao_001'

# Test scenarios
SCENARIOS = {
    'normal': {
        'name': 'Normal Air Quality',
        'e': [22.5, 45.3, 1013.25, 2.5, 750.0, 125.4, 45.2, 65.3],
        'pm': [12.5, 28.3, 35.1, 42.8, 50.0],
        'description': 'Typical moderate air quality'
    },
    'clean': {
        'name': 'Clean Air',
        'e': [20.0, 35.0, 1015.0, 1.5, 1000.0, 50.0, 10.0, 45.0],
        'pm': [3.0, 8.0, 12.0, 18.0, 25.0],
        'description': 'Good air quality - low PM levels'
    },
    'polluted': {
        'name': 'High Pollution',
        'e': [28.0, 65.0, 1012.0, 4.0, 600.0, 200.0, 80.0, 75.0],
        'pm': [40.0, 95.5, 120.0, 180.0, 250.0],
        'description': 'Poor air quality - high PM levels'
    },
    'hot': {
        'name': 'Hot & Humid',
        'e': [35.0, 70.0, 1010.0, 5.5, 500.0, 180.0, 70.0, 75.0],
        'pm': [25.0, 50.0, 65.0, 90.0, 120.0],
        'description': 'High temperature and humidity'
    },
    'cold': {
        'name': 'Cold & Dry',
        'e': [5.0, 20.0, 1020.0, 0.5, 1200.0, 30.0, 5.0, 40.0],
        'pm': [2.0, 5.0, 8.0, 12.0, 18.0],
        'description': 'Low temperature and humidity'
    }
}

def publish_payload(scenario_key, count=1):
    """Publish test payload"""
    
    if scenario_key not in SCENARIOS:
        print(f"Unknown scenario: {scenario_key}")
        print(f"Available: {', '.join(SCENARIOS.keys())}")
        return False
    
    scenario = SCENARIOS[scenario_key]
    
    print("\n" + "=" * 70)
    print(f"MQTTX Helper - Publishing {scenario['name']}")
    print("=" * 70)
    print(f"Scenario:     {scenario['name']}")
    print(f"Description:  {scenario['description']}")
    print(f"Broker:       {BROKER}:{PORT}")
    print(f"Topic:        {TOPIC}")
    print(f"Messages:     {count}")
    print()
    
    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("[CONNECT] Connected to broker")
        else:
            print(f"[ERROR] Connection failed: {rc}")
    
    def on_publish(client, userdata, mid, reason_code_list, properties):
        print(f"[PUBLISH] Message #{userdata['count']} published")
    
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f'mqttx-helper-{time.time()}')
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    try:
        print("Connecting to broker...")
        client.connect(BROKER, PORT, keepalive=60)
        client.loop_start()
        
        time.sleep(1)
        
        for i in range(count):
            payload = {
                'i': DEVICE_ID,
                'e': scenario['e'],
                'pm': scenario['pm'],
                'g': [51.5074, -0.1278, 45.2, 0.0],
                't': datetime.now().isoformat()
            }
            
            client.user_data_set({'count': i + 1})
            client.publish(TOPIC, json.dumps(payload), qos=1)
            
            print(f"\nMessage {i + 1}:")
            print(f"  PM2.5:       {payload['pm'][1]:.1f} µg/m³")
            print(f"  Temperature: {payload['e'][0]:.1f}°C")
            print(f"  Humidity:    {payload['e'][1]:.1f}%")
            print(f"  Timestamp:   {payload['t']}")
            
            if i < count - 1:
                time.sleep(2)
        
        print("\n" + "=" * 70)
        print("SUCCESS: All messages published!")
        print("=" * 70)
        print("\nExpected dashboard updates:")
        print("  ✓ Console: 'MQTT message received on xiao/dashboard'")
        print("  ✓ Charts update with new values")
        print("  ✓ Readings card refreshes")
        print()
        
        time.sleep(1)
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return False
    
    finally:
        client.loop_stop()
        client.disconnect()
        print("[DISCONNECT] Connection closed\n")
    
    return True

def show_scenarios():
    """Show available scenarios"""
    print("\nAvailable Scenarios:")
    print("=" * 70)
    for key, scenario in SCENARIOS.items():
        print(f"\n  {key}")
        print(f"    Name:        {scenario['name']}")
        print(f"    Description: {scenario['description']}")
        print(f"    PM2.5:       {scenario['pm'][1]:.1f} µg/m³")
        print(f"    Temperature: {scenario['e'][0]:.1f}°C")
        print(f"    Humidity:    {scenario['e'][1]:.1f}%")
    print("\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_scenarios()
        print("Usage: python mqttx_helper.py [scenario] [count]")
        print("\nExamples:")
        print("  python mqttx_helper.py normal           # Publish once")
        print("  python mqttx_helper.py clean            # Clean air scenario")
        print("  python mqttx_helper.py polluted 5       # 5 high pollution messages")
        print("  python mqttx_helper.py hot 3            # 3 hot/humid messages")
        sys.exit(1)
    
    scenario = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    success = publish_payload(scenario, count)
    sys.exit(0 if success else 1)
