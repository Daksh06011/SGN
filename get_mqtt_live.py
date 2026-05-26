#!/usr/bin/env python3
"""
Connect to MQTT broker and retrieve data
"""

import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
import threading

# MQTT Configuration from the image
MQTT_BROKER = "192.168.1.10"
MQTT_PORT = 1883
MQTT_TOPIC = "xiao/dashboard"
MQTT_USERNAME = None  # Optional
MQTT_PASSWORD = None  # Optional

# Global variables
messages = []
connected = False
message_count = 0
stop_flag = False

def on_connect(client, userdata, flags, rc, properties=None):
    """MQTT connection callback"""
    global connected
    
    if rc == 0:
        print("✅ Connected to MQTT broker successfully!")
        connected = True
        print(f"📡 Subscribing to topic: {MQTT_TOPIC}")
        client.subscribe(MQTT_TOPIC, qos=1)
    else:
        print(f"❌ Connection failed with code: {rc}")
        connected = False

def on_disconnect(client, userdata, rc):
    """MQTT disconnect callback"""
    global connected
    if rc != 0:
        print(f"⚠️  Unexpected disconnection. Code: {rc}")
    connected = False

def on_message(client, userdata, msg):
    """MQTT message callback"""
    global message_count, messages
    
    message_count += 1
    timestamp = datetime.now().isoformat()
    
    try:
        # Try to decode as JSON
        payload = json.loads(msg.payload.decode())
        is_json = True
    except:
        # If not JSON, store as string
        payload = msg.payload.decode()
        is_json = False
    
    message_data = {
        "count": message_count,
        "timestamp": timestamp,
        "topic": msg.topic,
        "qos": msg.qos,
        "retain": msg.retain,
        "payload": payload,
        "is_json": is_json,
        "payload_size": len(msg.payload)
    }
    
    messages.append(message_data)
    
    print(f"\n📨 Message #{message_count} received at {timestamp}")
    print(f"   Topic: {msg.topic}")
    print(f"   QoS: {msg.qos}, Retain: {msg.retain}")
    print(f"   Size: {len(msg.payload)} bytes")
    
    if is_json:
        print(f"   Data: {json.dumps(payload, indent=6)}")
    else:
        print(f"   Data: {payload}")

def on_subscribe(client, userdata, mid, reason_code_list, properties=None):
    """MQTT subscribe callback"""
    print(f"✅ Subscription confirmed for topic: {MQTT_TOPIC}")

def connect_and_listen(duration=30):
    """Connect to MQTT broker and listen for messages"""
    
    global stop_flag, messages, connected
    
    print("=" * 80)
    print("🔌 MQTT BROKER CONNECTION")
    print("=" * 80)
    print(f"🖥️  Broker:  {MQTT_BROKER}:{MQTT_PORT}")
    print(f"📡 Topic:   {MQTT_TOPIC}")
    print(f"⏱️  Timeout: {duration} seconds")
    print("=" * 80)
    print()
    
    # Create MQTT client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="python-subscriber")
    
    # Set callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    
    try:
        # Connect to broker
        print("🔗 Connecting to broker...")
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        
        # Start network loop
        client.loop_start()
        
        # Wait for connection
        start_time = time.time()
        while not connected and (time.time() - start_time) < 5:
            time.sleep(0.1)
        
        if not connected:
            print("❌ Failed to connect to broker")
            client.loop_stop()
            return None
        
        # Listen for messages
        print(f"\n👂 Listening for messages (timeout: {duration}s)...")
        print("   Press Ctrl+C to stop early\n")
        
        start_time = time.time()
        try:
            while (time.time() - start_time) < duration:
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n\n⏹️  Stopped by user")
        
        # Stop listening
        print("\n⏹️  Stopping listener...")
        client.loop_stop()
        client.disconnect()
        
        return messages
        
    except ConnectionRefusedError:
        print(f"❌ Connection refused - is the broker running at {MQTT_BROKER}:{MQTT_PORT}?")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def display_results(messages):
    """Display collected messages"""
    
    if not messages:
        print("❌ No messages received")
        return
    
    print("\n" + "=" * 80)
    print(f"📊 RECEIVED {len(messages)} MESSAGE(S)")
    print("=" * 80)
    print()
    
    for i, msg in enumerate(messages, 1):
        print(f"Message #{i}")
        print("-" * 80)
        print(f"⏰ Timestamp:  {msg['timestamp']}")
        print(f"📡 Topic:      {msg['topic']}")
        print(f"QoS: {msg['qos']}, Retain: {msg['retain']}, Size: {msg['payload_size']} bytes")
        print(f"\n📊 Payload:")
        
        if msg['is_json']:
            print(json.dumps(msg['payload'], indent=2))
        else:
            print(f"   {msg['payload']}")
        print()
    
    # Summary
    print("=" * 80)
    print("📈 SUMMARY")
    print("=" * 80)
    print(f"Total messages: {len(messages)}")
    print(f"Message rate: {len(messages) / 30:.2f} msg/s")
    
    if any(msg['is_json'] for msg in messages):
        print("\n📋 JSON Payload Structure (first JSON message):")
        for msg in messages:
            if msg['is_json']:
                print(json.dumps(msg['payload'], indent=2))
                break

if __name__ == "__main__":
    print("\n")
    messages = connect_and_listen(duration=30)
    
    if messages:
        display_results(messages)
    else:
        print("\n⚠️  Connection or data retrieval failed")
