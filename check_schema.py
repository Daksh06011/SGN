import sqlite3
db_path = "pm_monitoring.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
for table in ["dust_devices", "dust_sensor_data", "dust_extended_data"]:
    print(f"--- {table} ---")
    cursor.execute(f"PRAGMA table_info({table})")
    for col in cursor.fetchall():
        print(col)
conn.close()
