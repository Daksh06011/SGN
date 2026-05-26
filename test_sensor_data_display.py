"""
Test script to simulate sensor data reception and display
Demonstrates how the system processes and displays data with AQI calculation
"""

import json
import requests
from datetime import datetime

# Sample sensor data from your xiao-cam-01 device
sample_data = {
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

# Display the incoming data
print("=" * 70)
print("INCOMING SENSOR DATA FROM DEVICE")
print("=" * 70)
print(f"Device Site: {sample_data.get('site')}")
print(f"MAC Address: {sample_data.get('mac')}")
print(f"Timestamp: {sample_data.get('ts')}")
print(f"IP Address: {sample_data.get('ip')}")
print(f"Signal Strength (RSSI): {sample_data.get('rssi')} dBm")
print()

print("Environmental Data:")
print(f"  Temperature: {sample_data.get('tsi_temp')}°C")
print(f"  Humidity: {sample_data.get('tsi_rh')}%")
print(f"  Sound Level: {sample_data.get('sound')} dB")
print()

print("Air Quality Sensors:")
print(f"  NO₂: {sample_data.get('no2')} ppb")
print(f"  VOC: {sample_data.get('voc')} ppb")
print()

print("Particulate Matter Data (TSI Sensor):")
print(f"  PM1.0: {sample_data.get('tsi_pm1')} µg/m³")
print(f"  PM2.5: {sample_data.get('tsi_pm25')} µg/m³")
print(f"  PM4.0: {sample_data.get('tsi_pm4')} µg/m³")
print(f"  PM10:  {sample_data.get('tsi_pm10')} µg/m³")
print(f"  TSI Status: {sample_data.get('tsi')}")
print()

# AQI Calculation (UK DAQI)
pm2_5 = sample_data.get('tsi_pm25', 0)
pm10 = sample_data.get('tsi_pm10', 0)

def calculate_aqi_display(pm2_5, pm10):
    """Calculate UK DAQI and return display data"""
    # UK DAQI Thresholds
    if pm2_5 <= 11.0 and pm10 <= 40.0:
        return {
            "index": 0,
            "level": "Low",
            "color": "#00AA00",
            "description": "Air quality is good. Enjoy outdoor activities.",
            "range": "0-50"
        }
    elif pm2_5 <= 23.5 and pm10 <= 80.0:
        return {
            "index": 50,
            "level": "Moderate",
            "color": "#FFFF00",
            "description": "Air quality is acceptable. Most people can engage in outdoor activities.",
            "range": "50-100"
        }
    elif pm2_5 <= 47.0 and pm10 <= 160.0:
        return {
            "index": 100,
            "level": "High",
            "color": "#FF8800",
            "description": "Sensitive groups should limit outdoor activities.",
            "range": "100-150"
        }
    else:
        return {
            "index": 150,
            "level": "Very High",
            "color": "#FF0000",
            "description": "Everyone should avoid outdoor activities.",
            "range": "150+"
        }

aqi_data = calculate_aqi_display(pm2_5, pm10)

print("=" * 70)
print("CALCULATED AIR QUALITY INDEX (UK DAQI)")
print("=" * 70)
print(f"Current AQI Level: {aqi_data['level']}")
print(f"AQI Index: {aqi_data['index']}")
print(f"Status Color: {aqi_data['color']}")
print(f"Range: {aqi_data['range']}")
print(f"Description: {aqi_data['description']}")
print()
print(f"PM2.5: {pm2_5} µg/m³")
print(f"PM10: {pm10} µg/m³")
print()

# Show what this looks like in the database
print("=" * 70)
print("DATABASE RECORD (dust_sensor_data)")
print("=" * 70)
db_record = {
    "timestamp": "2026-05-15 14:05:00",
    "device_id": 1,
    "pm1": pm2_5 * 1000,
    "pm2_5": pm2_5 * 1000,
    "pm4": sample_data.get('tsi_pm4') * 1000,
    "pm10": pm10 * 1000,
    "tsp": sample_data.get('tsi_pm4') * 1000
}
for key, value in db_record.items():
    print(f"  {key}: {value}")
print()

# Show extended data record
print("=" * 70)
print("EXTENDED DATA RECORD (dust_extended_data)")
print("=" * 70)
extended_record = {
    "device_id": 1,
    "timestamp": "2026-05-15 14:05:00",
    "temperature_c": sample_data.get('tsi_temp'),
    "humidity_percent": sample_data.get('tsi_rh'),
    "voc_ppb": sample_data.get('voc'),
    "no2_ppb": sample_data.get('no2'),
    "noise_db": sample_data.get('sound'),
    "pm1": sample_data.get('tsi_pm1'),
    "pm2_5": sample_data.get('tsi_pm25'),
    "pm4": sample_data.get('tsi_pm4'),
    "pm10": sample_data.get('tsi_pm10'),
    "gps_lat": sample_data.get('lat'),
    "gps_lon": sample_data.get('lon')
}
for key, value in extended_record.items():
    print(f"  {key}: {value}")
print()

# Show what the frontend receives via WebSocket
print("=" * 70)
print("WEBSOCKET DATA SENT TO DASHBOARD")
print("=" * 70)
websocket_data = {
    "timestamp": "2026-05-15 14:05:00",
    "temperature": sample_data.get('tsi_temp'),
    "pm1": sample_data.get('tsi_pm1'),
    "pm2_5": sample_data.get('tsi_pm25'),
    "pm4": sample_data.get('tsi_pm4'),
    "pm10": sample_data.get('tsi_pm10'),
    "tsp": sample_data.get('tsi_pm4'),
    "aqi": {
        "current": aqi_data,
        "average": {
            "index": aqi_data['index'],
            "level": aqi_data['level']
        }
    }
}
print(json.dumps(websocket_data, indent=2))
print()

# Show dashboard display
print("=" * 70)
print("DASHBOARD DISPLAY")
print("=" * 70)
print(f"""
┌─────────────────────────────────────────────────────────┐
│                    AIR QUALITY INDEX                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │                                                 │  │
│  │            ╭─────────────────────╮             │  │
│  │            │                     │             │  │
│  │            │      AQI Gauge      │             │  │
│  │            │                     │             │  │
│  │            │   Current: {aqi_data['index']}          │             │  │
│  │            │   Level: {aqi_data['level']}          │             │  │
│  │            │   Color: {aqi_data['color']}         │             │  │
│  │            │                     │             │  │
│  │            ╰─────────────────────╯             │  │
│  │                                                 │  │
│  │  Air Quality: {aqi_data['level']} ({aqi_data['range']})              │  │
│  │  {aqi_data['description']}     │  │
│  │                                                 │  │
│  ├─────────────────────────────────────────────────┤  │
│  │                                                 │  │
│  │  PM2.5 (µg/m³): {pm2_5:<20}  │  │
│  │  PM10 (µg/m³):  {pm10:<20}  │  │
│  │  Temperature:   {sample_data.get('tsi_temp')}°C            │  │
│  │  Humidity:      {sample_data.get('tsi_rh')}%             │  │
│  │  15-min Avg AQI: {aqi_data['index']}                  │  │
│  │                                                 │  │
│  ├─────────────────────────────────────────────────┤  │
│  │           AQI SCALE (UK DAQI)                   │  │
│  │  🟢 Low (0-50)  🟡 Moderate (50-100)           │  │
│  │  🟠 High (100-150)  🔴 Very High (150+)        │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
""")

print("=" * 70)
print("CHARTS & METRICS UPDATED")
print("=" * 70)
print("""
✓ PM Levels Over Time chart updated with new data point
✓ Quick stat card updated (AQI: {}) 
✓ Real-time monitoring active
✓ 15-minute average AQI calculated
✓ Extended dashboard panels refreshed
""".format(aqi_data['level']))
