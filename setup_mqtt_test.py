#!/usr/bin/env python3
"""
Setup MQTT data source and test device for dashboard testing
"""

import sqlite3
import sys
from datetime import datetime

def setup_mqtt_test():
    """Initialize MQTT data source and test device"""
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('pm_monitoring.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        print("=" * 80)
        print("🔧 MQTT TEST SETUP")
        print("=" * 80)
        
        # 1. Check if admin user exists
        print("\n1️⃣  Checking for admin user...")
        cur.execute("SELECT id FROM dust_users WHERE is_admin = 1 LIMIT 1")
        admin = cur.fetchone()
        
        if not admin:
            print("   ❌ No admin user found. Creating default admin user...")
            # Create a default admin user (password: admin123)
            from werkzeug.security import generate_password_hash
            admin_hash = generate_password_hash('admin123')
            cur.execute(
                "INSERT INTO dust_users (username, email, password_hash, is_admin) VALUES (?, ?, ?, ?)",
                ('admin', 'admin@test.local', admin_hash, 1)
            )
            conn.commit()
            cur.execute("SELECT id FROM dust_users WHERE username = 'admin'")
            admin = cur.fetchone()
            print(f"   ✅ Admin user created (ID: {admin['id']})")
            admin_id = admin['id']
        else:
            admin_id = admin['id']
            print(f"   ✅ Admin user found (ID: {admin_id})")
        
        # 2. Add MQTT data source
        print("\n2️⃣  Adding MQTT data source...")
        cur.execute("SELECT id FROM dust_data_sources WHERE source_type = 'mqtt' LIMIT 1")
        existing_source = cur.fetchone()
        
        if existing_source:
            print(f"   ℹ️  MQTT source already exists (ID: {existing_source['id']})")
            mqtt_source_id = existing_source['id']
        else:
            cur.execute(
                """INSERT INTO dust_data_sources 
                   (source_type, broker_url, username, password, description) 
                   VALUES (?, ?, ?, ?, ?)""",
                ('mqtt', '192.168.1.10', '', '', 'Local Test MQTT Broker')
            )
            conn.commit()
            mqtt_source_id = cur.lastrowid
            print(f"   ✅ MQTT data source created (ID: {mqtt_source_id})")
            print(f"      Broker: 192.168.1.10:1883")
            print(f"      Topics: sensor/data, dustrak/status")
        
        # 3. Add test device
        print("\n3️⃣  Adding test device...")
        cur.execute(
            "SELECT id FROM dust_devices WHERE deviceid = 'xiao_001' LIMIT 1"
        )
        existing_device = cur.fetchone()
        
        if existing_device:
            print(f"   ℹ️  Test device already exists (ID: {existing_device['id']})")
            device_id = existing_device['id']
        else:
            cur.execute(
                """INSERT INTO dust_devices 
                   (deviceid, name, user_id, data_source_id, has_relay, location, description) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                ('xiao_001', 'Test Device (MQTT)', admin_id, mqtt_source_id, 0, 'Lab', 'MQTT test device')
            )
            conn.commit()
            device_id = cur.lastrowid
            print(f"   ✅ Test device created (ID: {device_id})")
            print(f"      Device ID: xiao_001")
            print(f"      Name: Test Device (MQTT)")
        
        # 4. Verify setup
        print("\n4️⃣  Verifying setup...")
        cur.execute("SELECT COUNT(*) as count FROM dust_devices WHERE data_source_id = ?", (mqtt_source_id,))
        device_count = cur.fetchone()['count']
        print(f"   ✅ {device_count} device(s) on MQTT data source")
        
        print("\n" + "=" * 80)
        print("✅ SETUP COMPLETE!")
        print("=" * 80)
        print("\n📋 Next steps:")
        print("   1. Start Flask app: python app.py")
        print("   2. In another terminal: python mqtt_publisher.py")
        print("   3. Open dashboard and select 'Test Device (MQTT)'")
        print("   4. Check for real-time PM data updates")
        print("\n💡 MQTT Message Format (compact):")
        print("""
        {
            "i": "xiao_001",
            "e": [temp, humidity, pressure, uv, lux, voc, no2, noise],
            "pm": [pm1, pm2.5, pm4, pm10, tsp],
            "g": [lat, lon, alt, speed],
            "t": "2024-01-01T12:00:00Z"
        }
        """)
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = setup_mqtt_test()
    sys.exit(0 if success else 1)
