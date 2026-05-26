#!/usr/bin/env python3
"""
Insert test MQTT data and configure data sources
"""

import os
import sqlite3
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json

load_dotenv()

USE_SQLITE = os.getenv('USE_SQLITE', 'true').lower() == 'true'

def setup_and_insert_test_data():
    """Set up MQTT data source and insert test data"""
    
    if USE_SQLITE:
        conn = sqlite3.connect('pm_monitoring.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    else:
        import psycopg2
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=int(os.getenv('DB_PORT', 5432))
        )
        cur = conn.cursor()
    
    try:
        print("=" * 80)
        print("🔧 SETTING UP MQTT DATA SOURCE AND TEST DATA")
        print("=" * 80)
        print()
        
        # 1. Create MQTT data source (if not exists)
        print("1️⃣  Creating MQTT Data Source...")
        
        cur.execute("""
            INSERT OR IGNORE INTO dust_data_sources 
            (source_type, broker_url, username, password, description)
            VALUES (?, ?, ?, ?, ?)
        """, (
            'mqtt',
            '192.168.1.10:1883',
            None,
            None,
            'Local MQTT Broker - xiao/dashboard'
        ))
        
        conn.commit()
        
        # Get the data source ID
        cur.execute("SELECT id FROM dust_data_sources WHERE broker_url = '192.168.1.10:1883' LIMIT 1")
        data_source = cur.fetchone()
        data_source_id = data_source['id'] if data_source else None
        
        if data_source_id:
            print(f"   ✅ Data source created with ID: {data_source_id}")
        else:
            print("   ❌ Failed to create data source")
            return
        
        # 2. Get or create a device
        print("\n2️⃣  Setting up test device...")
        
        device_id = "xiao_001"
        device_name = "XIAO Sensor Node - Dashboard"
        
        cur.execute("""
            INSERT OR IGNORE INTO dust_devices 
            (deviceid, name, data_source_id, location, description)
            VALUES (?, ?, ?, ?, ?)
        """, (
            device_id,
            device_name,
            data_source_id,
            "Laboratory / Test Environment",
            "XIAO microcontroller with environmental sensors"
        ))
        
        conn.commit()
        
        # Get device ID from database
        cur.execute("SELECT id FROM dust_devices WHERE deviceid = ? LIMIT 1", (device_id,))
        device = cur.fetchone()
        device_db_id = device['id'] if device else None
        
        if device_db_id:
            print(f"   ✅ Device created/found with DB ID: {device_db_id}")
        else:
            print("   ❌ Failed to set up device")
            return
        
        # 3. Insert test sensor data
        print("\n3️⃣  Inserting test sensor data...")
        
        test_records = [
            {
                "timestamp": datetime.now() - timedelta(hours=3),
                "pm1": 12.5,
                "pm2_5": 28.3,
                "pm4": 35.1,
                "pm10": 42.8,
                "tsp": 50.0
            },
            {
                "timestamp": datetime.now() - timedelta(hours=2),
                "pm1": 15.2,
                "pm2_5": 32.8,
                "pm4": 40.5,
                "pm10": 48.9,
                "tsp": 55.3
            },
            {
                "timestamp": datetime.now() - timedelta(hours=1),
                "pm1": 18.9,
                "pm2_5": 38.4,
                "pm4": 45.2,
                "pm10": 52.1,
                "tsp": 58.9
            },
            {
                "timestamp": datetime.now() - timedelta(minutes=30),
                "pm1": 22.1,
                "pm2_5": 42.7,
                "pm4": 50.3,
                "pm10": 58.5,
                "tsp": 65.2
            },
            {
                "timestamp": datetime.now(),
                "pm1": 20.5,
                "pm2_5": 39.8,
                "pm4": 47.2,
                "pm10": 54.6,
                "tsp": 62.1
            }
        ]
        
        for i, record in enumerate(test_records, 1):
            cur.execute("""
                INSERT INTO dust_sensor_data 
                (timestamp, device_id, data_source_id, pm1, pm2_5, pm4, pm10, tsp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record['timestamp'].isoformat(),
                device_db_id,
                data_source_id,
                record['pm1'],
                record['pm2_5'],
                record['pm4'],
                record['pm10'],
                record['tsp']
            ))
        
        conn.commit()
        print(f"   ✅ Inserted {len(test_records)} sensor data records")
        
        # 4. Insert extended data
        print("\n4️⃣  Inserting test extended environmental data...")
        
        extended_records = [
            {
                "timestamp": datetime.now() - timedelta(hours=3),
                "temperature_c": 22.5,
                "humidity_percent": 45.3,
                "pressure_hpa": 1013.25,
                "voc_ppb": 125.4,
                "no2_ppb": 45.2,
                "pm1": 12.5,
                "pm2_5": 28.3,
                "pm4": 35.1,
                "pm10": 42.8,
                "tsp_um": 50.0,
                "gps_lat": 51.5074,
                "gps_lon": -0.1278,
                "gps_alt_m": 45.2,
                "cloud_cover_percent": 30.0
            },
            {
                "timestamp": datetime.now() - timedelta(hours=2),
                "temperature_c": 23.1,
                "humidity_percent": 42.8,
                "pressure_hpa": 1012.95,
                "voc_ppb": 132.1,
                "no2_ppb": 48.7,
                "pm1": 15.2,
                "pm2_5": 32.8,
                "pm4": 40.5,
                "pm10": 48.9,
                "tsp_um": 55.3,
                "gps_lat": 51.5074,
                "gps_lon": -0.1278,
                "gps_alt_m": 45.2,
                "cloud_cover_percent": 35.0
            },
            {
                "timestamp": datetime.now() - timedelta(hours=1),
                "temperature_c": 24.2,
                "humidity_percent": 40.5,
                "pressure_hpa": 1012.50,
                "voc_ppb": 128.6,
                "no2_ppb": 51.2,
                "pm1": 18.9,
                "pm2_5": 38.4,
                "pm4": 45.2,
                "pm10": 52.1,
                "tsp_um": 58.9,
                "gps_lat": 51.5074,
                "gps_lon": -0.1278,
                "gps_alt_m": 45.2,
                "cloud_cover_percent": 40.0
            },
            {
                "timestamp": datetime.now() - timedelta(minutes=30),
                "temperature_c": 25.1,
                "humidity_percent": 38.2,
                "pressure_hpa": 1012.10,
                "voc_ppb": 135.3,
                "no2_ppb": 52.8,
                "pm1": 22.1,
                "pm2_5": 42.7,
                "pm4": 50.3,
                "pm10": 58.5,
                "tsp_um": 65.2,
                "gps_lat": 51.5074,
                "gps_lon": -0.1278,
                "gps_alt_m": 45.2,
                "cloud_cover_percent": 45.0
            },
            {
                "timestamp": datetime.now(),
                "temperature_c": 24.8,
                "humidity_percent": 39.5,
                "pressure_hpa": 1012.35,
                "voc_ppb": 131.2,
                "no2_ppb": 50.5,
                "pm1": 20.5,
                "pm2_5": 39.8,
                "pm4": 47.2,
                "pm10": 54.6,
                "tsp_um": 62.1,
                "gps_lat": 51.5074,
                "gps_lon": -0.1278,
                "gps_alt_m": 45.2,
                "cloud_cover_percent": 42.0
            }
        ]
        
        for i, record in enumerate(extended_records, 1):
            cur.execute("""
                INSERT INTO dust_extended_data 
                (device_id, timestamp, temperature_c, humidity_percent, pressure_hpa, 
                 voc_ppb, no2_ppb, pm1, pm2_5, pm4, pm10, tsp_um, gps_lat, gps_lon, 
                 gps_alt_m, cloud_cover_percent)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                device_db_id,
                record['timestamp'].isoformat(),
                record['temperature_c'],
                record['humidity_percent'],
                record['pressure_hpa'],
                record['voc_ppb'],
                record['no2_ppb'],
                record['pm1'],
                record['pm2_5'],
                record['pm4'],
                record['pm10'],
                record['tsp_um'],
                record['gps_lat'],
                record['gps_lon'],
                record['gps_alt_m'],
                record['cloud_cover_percent']
            ))
        
        conn.commit()
        print(f"   ✅ Inserted {len(extended_records)} extended data records")
        
        print("\n" + "=" * 80)
        print("✅ SETUP COMPLETE")
        print("=" * 80)
        print()
        print(f"📊 Summary:")
        print(f"   Data Source: {data_source_id} (192.168.1.10:1883)")
        print(f"   Device: {device_name} (ID: {device_db_id})")
        print(f"   Sensor Records: {len(test_records)}")
        print(f"   Extended Records: {len(extended_records)}")
        print()
        print("Now run: python get_mqtt_data.py")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    setup_and_insert_test_data()
