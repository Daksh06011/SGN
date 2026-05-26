#!/usr/bin/env python3
"""
Check MQTT configuration and available data
"""

import os
from dotenv import load_dotenv
import psycopg2
import sqlite3
from psycopg2.extras import RealDictCursor

load_dotenv()

# Database configuration
USE_SQLITE = os.getenv('USE_SQLITE', 'true').lower() == 'true'

def check_configuration():
    """Check MQTT configuration and data"""
    
    if USE_SQLITE:
        conn = sqlite3.connect('pm_monitoring.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    else:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=int(os.getenv('DB_PORT', 5432))
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        print("🔍 MQTT CONFIGURATION CHECK")
        print("=" * 80)
        
        # Check data sources
        print("\n1. 📡 DATA SOURCES (MQTT Brokers):")
        print("-" * 80)
        
        cur.execute("SELECT * FROM dust_data_sources WHERE source_type = 'mqtt'")
        data_sources = cur.fetchall()
        
        if not data_sources:
            print("   ❌ No MQTT data sources configured")
        else:
            for ds in data_sources:
                print(f"   ID: {ds['id']}")
                print(f"   Broker: {ds['broker_url']}")
                print(f"   Username: {ds['username']}")
                print(f"   Description: {ds['description']}")
                print()
        
        # Check devices
        print("\n2. 🎯 DEVICES:")
        print("-" * 80)
        
        cur.execute("""
            SELECT d.*, ds.broker_url 
            FROM dust_devices d 
            LEFT JOIN dust_data_sources ds ON d.data_source_id = ds.id
        """)
        devices = cur.fetchall()
        
        if not devices:
            print("   ❌ No devices configured")
        else:
            for dev in devices:
                print(f"   Device ID: {dev['deviceid']}")
                print(f"   Name: {dev['name']}")
                print(f"   Broker: {dev['broker_url']}")
                print(f"   Location: {dev['location']}")
                print(f"   Has Relay: {dev['has_relay']}")
                print()
        
        # Check users
        print("\n3. 👥 USERS:")
        print("-" * 80)
        
        cur.execute("SELECT id, username, email, is_admin FROM dust_users")
        users = cur.fetchall()
        
        if not users:
            print("   ❌ No users found")
        else:
            for user in users:
                admin_badge = "👑" if user['is_admin'] else "👤"
                print(f"   {admin_badge} {user['username']} ({user['email']})")
        
        # Check data counts
        print("\n4. 📊 DATA STATISTICS:")
        print("-" * 80)
        
        cur.execute("SELECT COUNT(*) as count FROM dust_sensor_data")
        sensor_count = cur.fetchone()['count']
        
        cur.execute("SELECT COUNT(*) as count FROM dust_extended_data")
        extended_count = cur.fetchone()['count']
        
        cur.execute("SELECT COUNT(*) as count FROM dust_device_alerts")
        alerts_count = cur.fetchone()['count']
        
        print(f"   Sensor data records: {sensor_count}")
        print(f"   Extended data records: {extended_count}")
        print(f"   Device alerts: {alerts_count}")
        
        if sensor_count > 0:
            cur.execute("SELECT MIN(timestamp) as earliest, MAX(timestamp) as latest FROM dust_sensor_data")
            time_range = cur.fetchone()
            print(f"   Data range: {time_range['earliest']} to {time_range['latest']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    check_configuration()
