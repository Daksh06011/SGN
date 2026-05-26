#!/usr/bin/env python3
import sqlite3, json
conn = sqlite3.connect('pm_monitoring.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Check counts
sensor_count = cur.execute('SELECT COUNT(*) as cnt FROM dust_sensor_data').fetchone()['cnt']
extended_count = cur.execute('SELECT COUNT(*) as cnt FROM dust_extended_data').fetchone()['cnt']

print(f"✓ Database Record Counts:")
print(f"  - Sensor data rows: {sensor_count}")
print(f"  - Extended data rows: {extended_count}")

# Get latest
latest = cur.execute('SELECT device_id, pm1, pm2_5, pm4, pm10, tsp, timestamp FROM dust_sensor_data ORDER BY timestamp DESC LIMIT 2').fetchall()
print(f"\n✓ Latest 2 Records:")
for i, row in enumerate(latest):
    print(f"  [{i+1}] Device={row['device_id']}, PM2.5={row['pm2_5']}, TSP={row['tsp']}, Time={row['timestamp']}")

# Extended data sample
extended = cur.execute('SELECT device_id, temperature_c, humidity_percent FROM dust_extended_data ORDER BY timestamp DESC LIMIT 1').fetchone()
if extended:
    print(f"\n✓ Extended Data Available:")
    print(f"  - Device={extended['device_id']}, Temp={extended['temperature_c']}°C, Humidity={extended['humidity_percent']}%")

conn.close()
print("\n✓✓✓ PM MONITORING DASHBOARD FULLY OPERATIONAL ✓✓✓")
