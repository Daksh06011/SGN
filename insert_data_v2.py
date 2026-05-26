import sqlite3
from datetime import datetime, timedelta

db_path = "pm_monitoring.db"
target_deviceid = "xiao_001"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get integer ID and data_source_id for xiao_001 from dust_devices
cursor.execute("SELECT id, data_source_id FROM dust_devices WHERE deviceid = ?", (target_deviceid,))
row = cursor.fetchone()
if not row:
    print(f"Device {target_deviceid} not found in dust_devices")
    conn.close()
    exit(1)
int_device_id, data_source_id = row

# Timestamps
now = datetime.now()
ts_now = now.isoformat(timespec='seconds').replace(" ", "T")
ts_prev = (now - timedelta(minutes=1)).isoformat(timespec='seconds').replace(" ", "T")

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
    # Insert into dust_sensor_data (device_id is integer FK to dust_devices.id)
    cursor.execute("""
        INSERT INTO dust_sensor_data (timestamp, device_id, data_source_id, pm1, pm2_5, pm4, pm10, tsp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ts, int_device_id, data_source_id, pm1, pm2_5, pm4, pm10, tsp))
    
    # Insert into dust_extended_data (device_id is integer FK to dust_devices.id)
    cursor.execute("""
        INSERT INTO dust_extended_data (timestamp, device_id, temperature_c, humidity_percent, pressure_hpa, voc_ppb, no2_ppb, noise_db, gps_lat, gps_lon)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ts, int_device_id, temp, hum, pres, voc, no2, noise, lat, lon))

conn.commit()
print(f"Successfully inserted rows for device {target_deviceid} (internal id {int_device_id}) at {ts_now} and {ts_prev}")
conn.close()
