import sqlite3
import os

def check_devices_sqlite():
    db_path = "pm_monitoring.db"
    if not os.path.exists(db_path):
        print(f"Database file {db_path} not found.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Check table columns
        cur.execute("PRAGMA table_info(dust_devices)")
        columns = cur.fetchall()
        print("Columns in dust_devices table:")
        for col in columns:
            print(f"  {col[1]}: {col[2]}")

        # Check what devices exist
        cur.execute("SELECT * FROM dust_devices")
        devices = cur.fetchall()
        
        # Get column names for display
        column_names = [description[0] for description in cur.description]
        print(f"\nRegistered devices ({len(devices)} found):")
        for device in devices:
            device_dict = dict(zip(column_names, device))
            print(device_dict)

    except Exception as e:
        print(f"Error checking devices table: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    check_devices_sqlite()
