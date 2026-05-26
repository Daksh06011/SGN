import sqlite3, json, time, ssl
try:
    import paho.mqtt.client as mqtt
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "paho-mqtt"])
    import paho.mqtt.client as mqtt

def run():
    try:
        conn = sqlite3.connect("pm_monitoring.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        cur.execute("PRAGMA table_info(dust_extended_data)")
        print("Columns:", [r["name"] for r in cur.fetchall()])
        
        cur.execute("SELECT id, deviceid FROM dust_devices WHERE deviceid IN ('xiao-cam-01', 'xiao-cam-02')")
        devices = [dict(r) for r in cur.fetchall()]
        print("Devices:", devices)
        
        client = mqtt.Client()
        client.username_pw_set("Daksh", "Sgn@1234")
        client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
        client.connect("fb1f89b92da34734b1ca59ef89f2dbfa.s1.eu.hivemq.cloud", 8883)
        
        for dev in devices:
            payload = json.dumps({"i": dev["deviceid"], "e": 1, "pm": 10.1, "g": "51.5,-0.1", "t": 20.0})
            client.publish("sensor/data", payload)
            print(f"Sent for {dev['deviceid']}")
            
        client.loop_start()
        time.sleep(3)
        client.loop_stop()
        client.disconnect()
        
        print("\nLast 6 Extended:")
        q5 = "SELECT d.deviceid, e.timestamp, e.temperature_c, e.humidity_percent, e.noise_db, e.lux, e.uv_index, e.gps_lat, e.gps_lon, e.pm2_5 FROM dust_extended_data e JOIN dust_devices d ON e.device_id = d.id ORDER BY e.id DESC LIMIT 6"
        for r in cur.execute(q5).fetchall(): print(dict(r))
        
        print("\nLast 6 Sensor:")
        q6 = "SELECT d.deviceid, s.timestamp, s.pm1, s.pm2_5, s.pm4, s.pm10, s.tsp FROM dust_sensor_data s JOIN dust_devices d ON s.device_id = d.id ORDER BY s.id DESC LIMIT 6"
        for r in cur.execute(q6).fetchall(): print(dict(r))
        
    except Exception as e: print(f"Error: {e}")
    finally:
        if "conn" in locals(): conn.close()
run()
