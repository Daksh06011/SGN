#!/usr/bin/env python3
"""
Insert payload into DB (create device if needed) and call emit_websocket_update(device_id)
"""
from datetime import datetime
import sys

import app

payload = {
    "site": "xiao-cam-01",
    "mac": "90:70:69:12:B9:CC",
    "ts": "2026-05-15 14:05:00",
    "ip": "192.168.31.221",
    "rssi": -69,
    "lat": 0,
    "lon": 0,
    "sound": 0,
    "no2": 0,
    "voc": 0,
    "tsi": "ok",
    "tsi_serial": "81432008054",
    "tsi_pm1": 7,
    "tsi_pm25": 7,
    "tsi_pm4": 7,
    "tsi_pm10": 7,
    "tsi_temp": 30.200000762939453,
    "tsi_rh": 72
}

# DB helpers
USE_SQLITE = app.USE_SQLITE

conn = None
try:
    conn = app.get_db_connection()
    cur = app.get_db_cursor(conn)

    # Ensure device exists in dust_devices
    if USE_SQLITE:
        cur.execute("SELECT id FROM dust_devices WHERE deviceid = ?", (payload['site'],))
    else:
        cur.execute("SELECT id FROM dust_devices WHERE deviceid = %s", (payload['site'],))
    row = cur.fetchone()
    if row:
        device_id_db = row[0] if isinstance(row, (list, tuple)) else (row['id'] if isinstance(row, dict) else row[0])
        print('Found device id:', device_id_db)
    else:
        # Insert device (assign to demo user 1 and data_source_id 1)
        if USE_SQLITE:
            cur.execute("INSERT INTO dust_devices (deviceid, name, user_id, data_source_id, has_relay, created_at) VALUES (?, ?, ?, ?, ?, datetime('now'))",
                        (payload['site'], payload['site'], 1, 1, 0))
            device_id_db = cur.lastrowid
        else:
            cur.execute("INSERT INTO dust_devices (deviceid, name, user_id, data_source_id, has_relay) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                        (payload['site'], payload['site'], 1, 1, False))
            device_id_db = cur.fetchone()['id']
        print('Inserted device id:', device_id_db)

    # Insert sensor row
    ts = payload['ts']
    # Convert to ISO format
    try:
        ts_dt = datetime.fromisoformat(ts.replace(' ', 'T'))
    except Exception:
        ts_dt = datetime.now()

    if USE_SQLITE:
        cur.execute(
            "INSERT INTO dust_sensor_data (timestamp, device_id, data_source_id, pm1, pm2_5, pm4, pm10, tsp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (ts_dt.isoformat(), device_id_db, 1, payload['tsi_pm1'], payload['tsi_pm25'], payload['tsi_pm4'], payload['tsi_pm10'], None)
        )
    else:
        cur.execute(
            "INSERT INTO dust_sensor_data (timestamp, device_id, data_source_id, pm1, pm2_5, pm4, pm10, tsp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (ts_dt, device_id_db, 1, payload['tsi_pm1'], payload['tsi_pm25'], payload['tsi_pm4'], payload['tsi_pm10'], None)
        )
    print('Inserted sensor data')

    # Insert extended data
    if USE_SQLITE:
        cur.execute(
            "INSERT INTO dust_extended_data (device_id, timestamp, temperature_c, humidity_percent, pressure_hpa, voc_ppb, no2_ppb, pm1, pm2_5, pm4, pm10, tsp_um, gps_lat, gps_lon, gps_alt_m, gps_speed_kmh, cloud_cover_percent) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (device_id_db, ts_dt.isoformat(), payload['tsi_temp'], payload['tsi_rh'], None, payload['voc'], payload['no2'], payload['tsi_pm1'], payload['tsi_pm25'], payload['tsi_pm4'], payload['tsi_pm10'], None, payload['lat'], payload['lon'], None, None, None)
        )
    else:
        cur.execute(
            "INSERT INTO dust_extended_data (device_id, timestamp, temperature_c, humidity_percent, pressure_hpa, voc_ppb, no2_ppb, pm1, pm2_5, pm4, pm10, tsp_um, gps_lat, gps_lon, gps_alt_m, gps_speed_kmh, cloud_cover_percent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (device_id_db, ts_dt, payload['tsi_temp'], payload['tsi_rh'], None, payload['voc'], payload['no2'], payload['tsi_pm1'], payload['tsi_pm25'], payload['tsi_pm4'], payload['tsi_pm10'], None, payload['lat'], payload['lon'], None, None, None)
        )
    print('Inserted extended data')

    # Commit
    conn.commit()
    # Ensure thresholds table exists (emit_websocket_update expects it)
    if USE_SQLITE:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS dust_thresholds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER REFERENCES dust_devices(id) ON DELETE CASCADE,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                pm1 REAL,
                pm2_5 REAL,
                pm4 REAL,
                pm10 REAL,
                tsp REAL,
                averaging_window INTEGER DEFAULT 15
            )
        ''')
        conn.commit()

    # Emit websocket update directly with constructed payload (avoid timestamp iso issues)
    websocket_data = {
        'device_id': payload['site'],
        'sensor': {
            'timestamp': ts_dt.isoformat(),
            'pm1': payload['tsi_pm1'],
            'pm2_5': payload['tsi_pm25'],
            'pm4': payload['tsi_pm4'],
            'pm10': payload['tsi_pm10'],
            'tsp': None,
            'temperature': payload['tsi_temp'],
            'humidity': payload['tsi_rh']
        },
        'extended': {
            'mac': payload['mac'],
            'ip': payload['ip'],
            'rssi': payload['rssi'],
            'lat': payload['lat'],
            'lon': payload['lon'],
            'sound': payload['sound'],
            'no2': payload['no2'],
            'voc': payload['voc'],
            'tsi': payload['tsi'],
            'tsi_serial': payload['tsi_serial']
        },
        'aqi': {
            'current': {'index': 0, 'level': 'Low', 'color': '#00AA00', 'pm2_5': payload['tsi_pm25'], 'pm10': payload['tsi_pm10']},
            'average': {'index': 0, 'level': 'Low'}
        }
    }

    print('Calling emit_device_update for device id', device_id_db)
    try:
        app.emit_device_update(device_id_db, websocket_data)
        print('Emit device update complete')
    except Exception as e:
        print('Emit failed:', e)
    print('Emit complete')

except Exception as e:
    print('Error:', e)
    if conn:
        conn.rollback()
    sys.exit(1)
finally:
    if conn:
        app.put_db_connection(conn)

print('Done')
