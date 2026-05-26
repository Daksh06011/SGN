#!/usr/bin/env python3
"""
Retrieve MQTT sensor data from the database
"""

import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import psycopg2
import sqlite3
from psycopg2.extras import RealDictCursor

load_dotenv()

# Database configuration
USE_SQLITE = os.getenv('USE_SQLITE', 'true').lower() == 'true'

def get_mqtt_data(hours=24, limit=100):
    """Get recent MQTT data from database"""
    
    if USE_SQLITE:
        # SQLite mode
        conn = sqlite3.connect('pm_monitoring.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    else:
        # PostgreSQL mode
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=int(os.getenv('DB_PORT', 5432))
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Get sensor data from the last N hours
        if USE_SQLITE:
            cur.execute(f"""
                SELECT 
                    s.id,
                    s.timestamp,
                    d.deviceid,
                    d.name as device_name,
                    s.pm1,
                    s.pm2_5,
                    s.pm4,
                    s.pm10,
                    s.tsp
                FROM dust_sensor_data s
                JOIN dust_devices d ON s.device_id = d.id
                WHERE s.timestamp > datetime('now', '-{hours} hours')
                ORDER BY s.timestamp DESC
                LIMIT {limit}
            """)
        else:
            cur.execute(f"""
                SELECT 
                    s.id,
                    s.timestamp,
                    d.deviceid,
                    d.name as device_name,
                    s.pm1,
                    s.pm2_5,
                    s.pm4,
                    s.pm10,
                    s.tsp
                FROM dust_sensor_data s
                JOIN dust_devices d ON s.device_id = d.id
                WHERE s.timestamp > NOW() - INTERVAL '{hours} hours'
                ORDER BY s.timestamp DESC
                LIMIT {limit}
            """)
        
        sensor_data = cur.fetchall()
        
        print("=" * 80)
        print(f"MQTT SENSOR DATA - Last {hours} hours (up to {limit} records)")
        print("=" * 80)
        
        if not sensor_data:
            print("❌ No sensor data found")
            return
        
        print(f"✅ Found {len(sensor_data)} records\n")
        
        for row in sensor_data:
            print(f"📡 Record ID: {row['id']}")
            print(f"   Device: {row['device_name']} (ID: {row['deviceid']})")
            print(f"   Timestamp: {row['timestamp']}")
            print(f"   PM1:    {row['pm1']} µg/m³")
            print(f"   PM2.5:  {row['pm2_5']} µg/m³")
            print(f"   PM4:    {row['pm4']} µg/m³")
            print(f"   PM10:   {row['pm10']} µg/m³")
            print(f"   TSP:    {row['tsp']} µg/m³")
            print()
        
        # Get extended data if available
        print("=" * 80)
        print("MQTT EXTENDED DATA - Environmental Parameters")
        print("=" * 80)
        
        if USE_SQLITE:
            cur.execute(f"""
                SELECT 
                    e.id,
                    e.timestamp,
                    d.deviceid,
                    d.name as device_name,
                    e.temperature_c,
                    e.humidity_percent,
                    e.pressure_hpa,
                    e.voc_ppb,
                    e.no2_ppb,
                    e.pm1,
                    e.pm2_5,
                    e.pm4,
                    e.pm10,
                    e.gps_lat,
                    e.gps_lon
                FROM dust_extended_data e
                JOIN dust_devices d ON e.device_id = d.id
                WHERE e.timestamp > datetime('now', '-{hours} hours')
                ORDER BY e.timestamp DESC
                LIMIT {limit}
            """)
        else:
            cur.execute(f"""
                SELECT 
                    e.id,
                    e.timestamp,
                    d.deviceid,
                    d.name as device_name,
                    e.temperature_c,
                    e.humidity_percent,
                    e.pressure_hpa,
                    e.voc_ppb,
                    e.no2_ppb,
                    e.pm1,
                    e.pm2_5,
                    e.pm4,
                    e.pm10,
                    e.gps_lat,
                    e.gps_lon
                FROM dust_extended_data e
                JOIN dust_devices d ON e.device_id = d.id
                WHERE e.timestamp > NOW() - INTERVAL '{hours} hours'
                ORDER BY e.timestamp DESC
                LIMIT {limit}
            """)
        
        extended_data = cur.fetchall()
        
        if not extended_data:
            print("❌ No extended data found")
        else:
            print(f"✅ Found {len(extended_data)} records\n")
            
            for row in extended_data:
                print(f"📊 Record ID: {row['id']}")
                print(f"   Device: {row['device_name']} (ID: {row['deviceid']})")
                print(f"   Timestamp: {row['timestamp']}")
                print(f"   🌡️  Temperature:  {row['temperature_c']}°C")
                print(f"   💧 Humidity:     {row['humidity_percent']}%")
                print(f"   🎚️  Pressure:     {row['pressure_hpa']} hPa")
                print(f"   💨 VOC:          {row['voc_ppb']} ppb")
                print(f"   ⚠️  NO2:          {row['no2_ppb']} ppb")
                print(f"   � GPS Lat:      {row['gps_lat']}°")
                print(f"   📍 GPS Lon:      {row['gps_lon']}°")
                print(f"   PM1/PM2.5/PM4/PM10: {row['pm1']}/{row['pm2_5']}/{row['pm4']}/{row['pm10']} µg/m³")
                print()
        
        # Summary statistics
        print("=" * 80)
        print("DATA SUMMARY")
        print("=" * 80)
        
        if USE_SQLITE:
            cur.execute(f"""
                SELECT 
                    COUNT(*) as total_records,
                    COUNT(DISTINCT device_id) as unique_devices,
                    AVG(pm2_5) as avg_pm2_5,
                    MAX(pm2_5) as max_pm2_5,
                    MIN(pm2_5) as min_pm2_5
                FROM dust_sensor_data
                WHERE timestamp > datetime('now', '-{hours} hours')
            """)
        else:
            cur.execute(f"""
                SELECT 
                    COUNT(*) as total_records,
                    COUNT(DISTINCT device_id) as unique_devices,
                    AVG(pm2_5) as avg_pm2_5,
                    MAX(pm2_5) as max_pm2_5,
                    MIN(pm2_5) as min_pm2_5
                FROM dust_sensor_data
                WHERE timestamp > NOW() - INTERVAL '{hours} hours'
            """)
        
        stats = cur.fetchone()
        print(f"Total records: {stats['total_records']}")
        print(f"Unique devices: {stats['unique_devices']}")
        print(f"Average PM2.5: {stats['avg_pm2_5']:.2f} µg/m³")
        print(f"Max PM2.5: {stats['max_pm2_5']:.2f} µg/m³")
        print(f"Min PM2.5: {stats['min_pm2_5']:.2f} µg/m³")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    import sys
    
    hours = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    
    get_mqtt_data(hours=hours, limit=limit)
