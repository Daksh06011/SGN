#!/usr/bin/env python3
"""
Visual Display of xiao-cam-01 Sensor Data on Dashboard
Shows exactly where and how the data appears in the UI
"""

import json
from datetime import datetime

# Your sensor data (normalized - using first of each duplicate key)
sensor_data = {
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

# Calculate AQI
pm2_5 = sensor_data['tsi_pm25']
pm10 = sensor_data['tsi_pm10']

if pm2_5 <= 11.0 and pm10 <= 40.0:
    aqi_level = "Low"
    aqi_index = 0
    aqi_color = "#00AA00"
    aqi_emoji = "🟢"
elif pm2_5 <= 23.5 and pm10 <= 80.0:
    aqi_level = "Moderate"
    aqi_index = 50
    aqi_color = "#FFFF00"
    aqi_emoji = "🟡"
elif pm2_5 <= 47.0 and pm10 <= 160.0:
    aqi_level = "High"
    aqi_index = 100
    aqi_color = "#FF8800"
    aqi_emoji = "🟠"
else:
    aqi_level = "Very High"
    aqi_index = 150
    aqi_color = "#FF0000"
    aqi_emoji = "🔴"

# Clear screen and show dashboard
print("\033[2J\033[H")  # Clear screen
print()
print("╔" + "═" * 102 + "╗")
print("║" + " " * 102 + "║")
print("║" + "SGN CONTROLS v2.0 - ENVIRONMENTAL MONITOR".center(102) + "║")
print("║" + "Real-time Air Quality & Particulate Matter Monitoring".center(102) + "║")
print("║" + " " * 102 + "║")
print("╚" + "═" * 102 + "╝")
print()

# SECTION 1: QUICK STATS
print("┌" + "─" * 102 + "┐")
print("│ " + "QUICK STATS (Header Row)".ljust(100) + " │")
print("├" + "─" * 102 + "┤")
print("│ " + " " * 100 + " │")

stats_line = f"│  Devices: 1  │  Online: 1  │  Alerts: 0  │  Avg PM2.5: {pm2_5} µg/m³  │  Max Temp: {sensor_data['tsi_temp']:.1f}°C  │  Last Update: {sensor_data['ts']}  │  AQI: {aqi_emoji} {aqi_index} ({aqi_level})"
stats_line = stats_line.ljust(102) + " │"
print(stats_line)
print("│ " + " " * 100 + " │")
print("└" + "─" * 102 + "┘")
print()

# SECTION 2: TEMPERATURE
print("┌" + "─" * 102 + "┐")
print("│ " + "LIVE TEMPERATURE".ljust(100) + " │")
print("├" + "─" * 102 + "┤")
print("│ " + " " * 100 + " │")
print(f"│  {sensor_data['tsi_temp']:.1f}°C".ljust(103) + "│")
print("│  Current Temperature Reading from xiao-cam-01 (TSI Sensor)".ljust(103) + "│")
print("│ " + " " * 100 + " │")
print("└" + "─" * 102 + "┘")
print()

# SECTION 3: DEVICE SELECTION & DATA EXPORT
print("┌" + "─" * 102 + "┐")
print("│ " + "DEVICE SELECTION & DATA EXPORT".ljust(100) + " │")
print("├" + "─" * 50 + "┬" + "─" * 50 + "┤")
print("│ " + "DEVICE SELECTION".center(48) + " │ " + "DATA EXPORT".center(48) + " │")
print("├" + "─" * 50 + "┼" + "─" * 50 + "┤")
print("│ " + " " * 48 + " │ " + " " * 48 + " │")
print("│  Select Device:".ljust(50) + " │ " + "From: 2026-05-10".ljust(49) + " │")
print("│  [xiao-cam-01              ▼]".ljust(50) + " │ " + "To:   2026-05-17".ljust(49) + " │")
print("│  [Refresh] [Auto]".ljust(50) + " │ " + "[📥 Export CSV]".ljust(49) + " │")
print("│ " + " " * 48 + " │ " + " " * 48 + " │")
print("└" + "─" * 50 + "┴" + "─" * 50 + "┘")
print()

# SECTION 4: AIR QUALITY INDEX (MAIN SECTION)
print("┌" + "─" * 102 + "┐")
print("│ " + "AIR QUALITY INDEX ⭐ (Positioned Below Device Selection)".ljust(100) + " │")
print("│ " + "UK DAQI Standard".ljust(100) + " │")
print("├" + "─" * 102 + "┤")
print("│ " + " " * 100 + " │")

# Left: Gauge
gauge_color = "🟢" if aqi_color == "#00AA00" else "🟡" if aqi_color == "#FFFF00" else "🟠" if aqi_color == "#FF8800" else "🔴"
print(f"│  ╭──────────────────────────╮     Current Status: {aqi_emoji} {aqi_level.upper()}".ljust(103) + "│")
print(f"│  │                          │     Air quality level: {aqi_level}".ljust(103) + "│")
print(f"│  │        AQI GAUGE         │     ".ljust(103) + "│")
print(f"│  │                          │     PM2.5: {pm2_5} µg/m³ (Threshold for Low: ≤ 11.0)".ljust(103) + "│")
print(f"│  │      Index: {aqi_index}       │     PM10:  {pm10} µg/m³ (Threshold for Low: ≤ 40.0)".ljust(103) + "│")
print(f"│  │      Level: {aqi_level.ljust(10)}│     ".ljust(103) + "│")
print(f"│  │      Color: {aqi_color}  │     15-min Avg AQI: {aqi_index} ({aqi_level})".ljust(103) + "│")
print(f"│  │    Border: {gauge_color}  │     ".ljust(103) + "│")
print(f"│  ╰──────────────────────────╯     Description: Air quality is good. Enjoy outdoor activities.".ljust(103) + "│")
print("│ " + " " * 100 + " │")
print("├" + "─" * 102 + "┤")
print("│ " + "AQI SCALE (UK DAQI)".ljust(100) + " │")
print("│ " + " " * 100 + " │")
print("│  ┌─────────────┬──────────────────┬──────────────────┬──────────────────────┐".ljust(103) + "│")
print("│  │   🟢 LOW    │  🟡 MODERATE     │    🟠 HIGH       │   🔴 VERY HIGH       │".ljust(103) + "│")
print("│  │   0-50 µ    │    50-100 µ      │   100-150 µ      │      150+ µ          │".ljust(103) + "│")
print("│  └─────────────┴──────────────────┴──────────────────┴──────────────────────┘".ljust(103) + "│")
print("│ " + " " * 100 + " │")
print("└" + "─" * 102 + "┘")
print()

# SECTION 5: DEVICE INFORMATION PANEL
print("┌" + "─" * 102 + "┐")
print("│ " + "DEVICE INFORMATION PANEL".ljust(100) + " │")
print("├" + "─" * 102 + "┤")
print(f"│  Device: {sensor_data['site']}".ljust(103) + "│")
print(f"│  MAC Address: {sensor_data['mac']}".ljust(103) + "│")
print(f"│  IP Address: {sensor_data['ip']}".ljust(103) + "│")
print(f"│  Signal Strength: {sensor_data['rssi']} dBm (Good)".ljust(103) + "│")
print(f"│  Last Update: {sensor_data['ts']}".ljust(103) + "│")
print(f"│  Status: ✅ Online and Sending Data".ljust(103) + "│")
print("│ " + " " * 100 + " │")
print("└" + "─" * 102 + "┘")
print()

# SECTION 6: SENSOR READINGS TABLE
print("┌" + "─" * 102 + "┐")
print("│ " + "REAL-TIME SENSOR READINGS".ljust(100) + " │")
print("├" + "─" * 102 + "┤")
print("│ " + " " * 100 + " │")

readings = [
    ("Environmental Data:", ""),
    ("  Temperature", f"{sensor_data['tsi_temp']:.2f}°C"),
    ("  Humidity", f"{sensor_data['tsi_rh']}%"),
    ("  Sound Level", f"{sensor_data['sound']} dB"),
    ("", ""),
    ("Particulate Matter (PM):", ""),
    ("  PM1.0", f"{sensor_data['tsi_pm1']} µg/m³"),
    ("  PM2.5 ⭐", f"{sensor_data['tsi_pm25']} µg/m³ (Used for AQI)"),
    ("  PM4.0", f"{sensor_data['tsi_pm4']} µg/m³"),
    ("  PM10 ⭐", f"{sensor_data['tsi_pm10']} µg/m³ (Used for AQI)"),
    ("", ""),
    ("Air Quality Sensors:", ""),
    ("  NO₂", f"{sensor_data['no2']} ppb"),
    ("  VOC", f"{sensor_data['voc']} ppb"),
    ("", ""),
    ("Device Status:", ""),
    ("  TSI Status", sensor_data['tsi']),
    ("  TSI Serial", sensor_data['tsi_serial']),
    ("  Location", f"({sensor_data['lat']}, {sensor_data['lon']})"),
]

for label, value in readings:
    if label == "":
        print("│ " + " " * 100 + " │")
    elif not value:
        print(f"│  {label}".ljust(103) + "│")
    else:
        print(f"│  {label:<30} {value}".ljust(103) + "│")

print("│ " + " " * 100 + " │")
print("└" + "─" * 102 + "┘")
print()

# SECTION 7: DATA FLOW VISUALIZATION
print("┌" + "─" * 102 + "┐")
print("│ " + "DATA FLOW VISUALIZATION".ljust(100) + " │")
print("├" + "─" * 102 + "┤")
print("│ " + " " * 100 + " │")
print("│  Device → MQTT Broker → Flask Backend → Database → WebSocket → Browser Dashboard".ljust(103) + "│")
print("│   ↓           ↓              ↓              ↓           ↓              ↓".ljust(103) + "│")
print("│ xiao-cam- Receives      Parses &      Stores in    Emits via   Updates UI".ljust(103) + "│")
print("│  01       JSON         Validates      SQLite/      Socket.IO   in Real-Time".ljust(103) + "│")
print("│                        AQI Calc       PostgreSQL   (< 500ms)".ljust(103) + "│")
print("│ " + " " * 100 + " │")
print("└" + "─" * 102 + "┘")
print()

# SECTION 8: CHARTS & ANALYTICS
print("┌" + "─" * 102 + "┐")
print("│ " + "CHARTS & ANALYTICS (Overview Tab)".ljust(100) + " │")
print("├" + "─" * 102 + "┤")
print("│ " + " " * 100 + " │")
print("│  PM LEVELS OVER TIME".ljust(103) + "│")
print("│  µg/m³                                                              [Current] [15-min Avg]".ljust(103) + "│")
print("│    │     ".ljust(103) + "│")
print("│   20│  ●  ← New data point added".ljust(103) + "│")
print("│    │  /╲ ".ljust(103) + "│")
print("│   10│_/  ╲  ← Real-time updates".ljust(103) + "│")
print("│    │      ╲".ljust(103) + "│")
print("│    └──────────────────────────────────────────────────────────────────".ljust(103) + "│")
print("│      14:00  14:05  14:10  14:15  14:20  14:25  14:30  14:35  14:40".ljust(103) + "│")
print("│ " + " " * 100 + " │")
print("│  Current PM Levels (14:05:00)".ljust(103) + "│")
print(f"│  PM1: {sensor_data['tsi_pm1']} µg/m³  │  PM2.5: {sensor_data['tsi_pm25']} µg/m³  │  PM4: {sensor_data['tsi_pm4']} µg/m³  │  PM10: {sensor_data['tsi_pm10']} µg/m³  │  TSP: {sensor_data['tsi_pm4']} µg/m³".ljust(103) + "│")
print("│ " + " " * 100 + " │")
print("│  Air Quality Index Panel".ljust(103) + "│")
print(f"│  Current: {aqi_index} ({aqi_level})  │  15-min Avg: {aqi_index} ({aqi_level})  │  Status: {aqi_emoji} {aqi_level.upper()}".ljust(103) + "│")
print("│ " + " " * 100 + " │")
print("└" + "─" * 102 + "┘")
print()

# SECTION 9: STATUS & UPDATES
print("┌" + "─" * 102 + "┐")
print("│ " + "SYSTEM STATUS & ACTIONS COMPLETED".ljust(100) + " │")
print("├" + "─" * 102 + "┤")
print("│ " + " " * 100 + " │")
print("│  ✅ Sensor Data Received".ljust(103) + "│")
print("│  ✅ Device Authenticated (xiao-cam-01)".ljust(103) + "│")
print("│  ✅ AQI Calculated: 🟢 LOW (Index: 0)".ljust(103) + "│")
print("│  ✅ Database Records Stored (dust_sensor_data & dust_extended_data)".ljust(103) + "│")
print("│  ✅ WebSocket Update Emitted to Connected Clients".ljust(103) + "│")
print("│  ✅ Dashboard Display Updated in Real-Time".ljust(103) + "│")
print("│  ✅ Charts Refreshed with New Data Points".ljust(103) + "│")
print("│  ✅ All Metrics Displayed (Temperature, Humidity, PM Values, AQI)".ljust(103) + "│")
print("│ " + " " * 100 + " │")
print("└" + "─" * 102 + "┘")
print()

# SECTION 10: SUMMARY
print("┌" + "─" * 102 + "┐")
print("│ " + "DATA SUMMARY".ljust(100) + " │")
print("├" + "─" * 102 + "┤")
print("│ " + " " * 100 + " │")
print(f"│  Device:         {sensor_data['site']} (MAC: {sensor_data['mac']})".ljust(103) + "│")
print(f"│  Timestamp:      {sensor_data['ts']}".ljust(103) + "│")
print(f"│  IP Address:     {sensor_data['ip']}".ljust(103) + "│")
print("│ " + " " * 100 + " │")
print(f"│  Temperature:    {sensor_data['tsi_temp']:.2f}°C".ljust(103) + "│")
print(f"│  Humidity:       {sensor_data['tsi_rh']}%".ljust(103) + "│")
print(f"│  PM2.5:          {sensor_data['tsi_pm25']} µg/m³".ljust(103) + "│")
print(f"│  PM10:           {sensor_data['tsi_pm10']} µg/m³".ljust(103) + "│")
print("│ " + " " * 100 + " │")
print(f"│  AQI Level:      {aqi_emoji} {aqi_level.upper()}".ljust(103) + "│")
print(f"│  AQI Index:      {aqi_index}".ljust(103) + "│")
print(f"│  AQI Color:      {aqi_color}".ljust(103) + "│")
print(f"│  Signal Quality: {sensor_data['rssi']} dBm (Good Connection)".ljust(103) + "│")
print("│ " + " " * 100 + " │")
print("└" + "─" * 102 + "┘")
print()
print("✨ System Ready for Real-Time Monitoring! 🎉")
print()
