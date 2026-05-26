#!/usr/bin/env python3
"""Update MQTT broker configuration to use HiveMQ cloud"""

import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('pm_monitoring.db')
cursor = conn.cursor()

# HiveMQ Cloud Configuration (from mqtt_publisher.py defaults)
MQTT_BROKER = "fb1f89b92da34734b1ca59ef89f2dbfa.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "Daksh"
MQTT_PASSWORD = "Sgn@1234"
MQTT_TOPIC = "xiao/dashboard"

print("=" * 80)
print("📡 UPDATING MQTT BROKER CONFIGURATION")
print("=" * 80)
print(f"🖥️  Broker:   {MQTT_BROKER}:{MQTT_PORT}")
print(f"📝 Username: {MQTT_USERNAME}")
print(f"🔐 Topic:    {MQTT_TOPIC}")
print()

# Update both data sources to use HiveMQ
for data_source_id in [1, 2]:
    cursor.execute("""
        UPDATE dust_data_sources
        SET broker_url = ?, port = ?, username = ?, password = ?, topic = ?
        WHERE id = ?
    """, (MQTT_BROKER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, MQTT_TOPIC, data_source_id))
    print(f"✅ Updated data source {data_source_id}")

conn.commit()

# Verify the update
print("\n" + "=" * 80)
print("📋 VERIFICATION")
print("=" * 80)
cursor.execute("SELECT id, broker_url, port, username, password, topic FROM dust_data_sources;")
rows = cursor.fetchall()
for row in rows:
    print(f"\nData Source {row[0]}:")
    print(f"  Broker: {row[1]}:{row[2]}")
    print(f"  Username: {row[3]}")
    print(f"  Password: {'*' * len(row[4]) if row[4] else 'None'}")
    print(f"  Topic: {row[5]}")

conn.close()
print("\n✨ Configuration updated successfully!")
print("\n💡 Note: You need to RESTART the Flask app for changes to take effect!")
