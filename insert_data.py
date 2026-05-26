import sqlite3
from datetime import datetime, timedelta

db_path = "pm_monitoring.db"
device_id = "xiao_001"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get data_source_id for xiao_001
cursor.execute("SELECT data_source_id FROM dust_devices WHERE device_id = ?", (device_id,))
row = cursor.fetchone()
if not row:
    print(f"Device {device_id} not found in dust_devices")
    conn.close()
    exit(1)
data_source_id = row[0]

# Timestamps
now = datetime.now()
ts_now = now.isoformat(timespec='seconds')
ts_prev = (now - timedelta(minutes=1)).isoformat(timespec='seconds')

timestamps = [ts_now, ts_prev]

# Data values
pm1, pm2_5, pm4, pm10, tsp = 7, 7, 7, 7, 7
temp = 30.200000762939453
hum = 72
pres = 0
voc = 0
no2 = 0
noise = 0
lat = 0
lon = 0

for ts in timestamps:
    # Insert into dust_sensor_data
    cursor.execute("""
        INSERT INTO dust_sensor_data (timestamp, device_id, data_source_id, pm1, pm2_5, pm4, pm10, tsp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ts, device_id, data_source_id, pm1, pm2_5, pm4, pm10, tsp))
    
    # Insert into dust_extended_data
    cursor.execute("""
        INSERT INTO dust_extended_data (timestamp, device_id, data_source_id, temperature_c, humidity_percent, pressure_hpa, voc_ppb, no2_ppb, noise_db, gps_lat, gps_lon)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ts, device_id, data_source_id, temp, hum, pres, voc, no2, noise, lat, lon))

conn.commit()
print(f"Successfully inserted rows for device {device_id} at {ts_now} and {ts_prev}")
conn.close()
