#!/usr/bin/env python3
"""Make a user admin and/or assign devices to them"""

import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

USE_SQLITE = os.getenv('USE_SQLITE', 'true').lower() == 'true'

if USE_SQLITE:
    sqlite_db_path = 'pm_monitoring.db'
    conn = sqlite3.connect(sqlite_db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    # Make user admin
    username = 'demouser123'
    cur.execute("UPDATE dust_users SET is_admin = 1 WHERE username = ?", (username,))
    conn.commit()
    
    # Check if update worked
    cur.execute("SELECT id, username, is_admin FROM dust_users WHERE username = ?", (username,))
    user = cur.fetchone()
    if user:
        print(f"✅ User '{user['username']}' is now admin: {bool(user['is_admin'])}")
        user_id = user['id']
        
        # Assign all devices to this user
        cur.execute("UPDATE dust_devices SET user_id = ? WHERE user_id IS NULL", (user_id,))
        conn.commit()
        
        # Show devices
        cur.execute("SELECT id, deviceid, name FROM dust_devices WHERE user_id = ?", (user_id,))
        devices = cur.fetchall()
        print(f"\n📱 Assigned {len(devices)} device(s) to user:")
        for device in devices:
            print(f"   - {device['deviceid']}: {device['name']}")
    else:
        print(f"❌ User '{username}' not found")
    
    conn.close()
else:
    print("This script is for SQLite only")
