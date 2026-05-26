#!/usr/bin/env python3
"""
Sample MQTT Data - Demonstrates the data structure received from MQTT clients
"""

import json
from datetime import datetime, timedelta
import random

# Sample MQTT messages received from devices
SAMPLE_MQTT_DATA = [
    {
        "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
        "device": {
            "id": "1225",
            "name": "UK Office Monitor",
            "location": "London, UK"
        },
        "sensor_data": {
            "pm1": 12.5,
            "pm2_5": 28.3,
            "pm4": 35.1,
            "pm10": 42.8,
            "tsp": 50.0
        },
        "extended_data": {
            "temperature_c": 22.5,
            "humidity_percent": 45.3,
            "pressure_hpa": 1013.25,
            "voc_ppb": 125.4,
            "no2_ppb": 45.2,
            "noise_db": 65.3,
            "gps_lat": 51.5074,
            "gps_lon": -0.1278,
            "gps_alt_m": 45.2,
            "cloud_cover_percent": 30
        }
    },
    {
        "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
        "device": {
            "id": "1225",
            "name": "UK Office Monitor",
            "location": "London, UK"
        },
        "sensor_data": {
            "pm1": 15.2,
            "pm2_5": 32.8,
            "pm4": 40.5,
            "pm10": 48.9,
            "tsp": 55.3
        },
        "extended_data": {
            "temperature_c": 23.1,
            "humidity_percent": 42.8,
            "pressure_hpa": 1012.95,
            "voc_ppb": 132.1,
            "no2_ppb": 48.7,
            "noise_db": 67.2,
            "gps_lat": 51.5074,
            "gps_lon": -0.1278,
            "gps_alt_m": 45.2,
            "cloud_cover_percent": 35
        }
    },
    {
        "timestamp": datetime.now().isoformat(),
        "device": {
            "id": "1225",
            "name": "UK Office Monitor",
            "location": "London, UK"
        },
        "sensor_data": {
            "pm1": 18.9,
            "pm2_5": 38.4,
            "pm4": 45.2,
            "pm10": 52.1,
            "tsp": 58.9
        },
        "extended_data": {
            "temperature_c": 24.2,
            "humidity_percent": 40.5,
            "pressure_hpa": 1012.50,
            "voc_ppb": 128.6,
            "no2_ppb": 51.2,
            "noise_db": 69.1,
            "gps_lat": 51.5074,
            "gps_lon": -0.1278,
            "gps_alt_m": 45.2,
            "cloud_cover_percent": 40
        }
    }
]

def print_mqtt_data():
    """Display sample MQTT data in a formatted way"""
    
    print("=" * 100)
    print("📡 SAMPLE MQTT SENSOR DATA - UK PM MONITORING SYSTEM")
    print("=" * 100)
    print()
    
    for i, record in enumerate(SAMPLE_MQTT_DATA, 1):
        print(f"Record #{i}")
        print("-" * 100)
        print(f"⏰ Timestamp:  {record['timestamp']}")
        print(f"🎯 Device:     {record['device']['name']} (ID: {record['device']['id']})")
        print(f"📍 Location:   {record['device']['location']}")
        print()
        
        print("📊 SENSOR DATA (Particulate Matter):")
        sensor = record['sensor_data']
        print(f"   PM1:    {sensor['pm1']:>6.1f} µg/m³  ← Fine particulates")
        print(f"   PM2.5:  {sensor['pm2_5']:>6.1f} µg/m³  ← Health-relevant particulates")
        print(f"   PM4:    {sensor['pm4']:>6.1f} µg/m³")
        print(f"   PM10:   {sensor['pm10']:>6.1f} µg/m³  ← Coarse particulates")
        print(f"   TSP:    {sensor['tsp']:>6.1f} µg/m³  ← Total Suspended Particulates")
        print()
        
        print("🌡️  EXTENDED ENVIRONMENTAL DATA:")
        ext = record['extended_data']
        print(f"   Temperature:    {ext['temperature_c']:>6.1f} °C")
        print(f"   Humidity:       {ext['humidity_percent']:>6.1f} %")
        print(f"   Pressure:       {ext['pressure_hpa']:>6.2f} hPa")
        print(f"   VOC:            {ext['voc_ppb']:>6.1f} ppb  (Volatile Organic Compounds)")
        print(f"   NO2:            {ext['no2_ppb']:>6.1f} ppb  (Nitrogen Dioxide)")
        print(f"   Noise Level:    {ext['noise_db']:>6.1f} dB")
        print(f"   GPS Lat:        {ext['gps_lat']:>10.4f}°")
        print(f"   GPS Lon:        {ext['gps_lon']:>10.4f}°")
        print(f"   GPS Alt:        {ext['gps_alt_m']:>6.1f} meters")
        print(f"   Cloud Cover:    {ext['cloud_cover_percent']:>6.1f} %")
        print()
    
    # Display as JSON format
    print("=" * 100)
    print("JSON FORMAT (Raw MQTT Payload):")
    print("=" * 100)
    print(json.dumps(SAMPLE_MQTT_DATA, indent=2))
    print()
    
    # Display statistics
    print("=" * 100)
    print("📈 DATA SUMMARY & STATISTICS")
    print("=" * 100)
    
    pm25_values = [r['sensor_data']['pm2_5'] for r in SAMPLE_MQTT_DATA]
    temp_values = [r['extended_data']['temperature_c'] for r in SAMPLE_MQTT_DATA]
    voc_values = [r['extended_data']['voc_ppb'] for r in SAMPLE_MQTT_DATA]
    
    print(f"\n📊 PM2.5 (Fine Particulates):")
    print(f"   Average: {sum(pm25_values)/len(pm25_values):.1f} µg/m³")
    print(f"   Min:     {min(pm25_values):.1f} µg/m³")
    print(f"   Max:     {max(pm25_values):.1f} µg/m³")
    print(f"   Trend:   {'↑ Increasing' if pm25_values[-1] > pm25_values[0] else '↓ Decreasing'}")
    
    print(f"\n🌡️  Temperature:")
    print(f"   Average: {sum(temp_values)/len(temp_values):.1f} °C")
    print(f"   Min:     {min(temp_values):.1f} °C")
    print(f"   Max:     {max(temp_values):.1f} °C")
    
    print(f"\n💨 VOC (Air Quality Indicator):")
    print(f"   Average: {sum(voc_values)/len(voc_values):.1f} ppb")
    print(f"   Min:     {min(voc_values):.1f} ppb")
    print(f"   Max:     {max(voc_values):.1f} ppb")
    
    print(f"\nℹ️  Data Points: {len(SAMPLE_MQTT_DATA)} records")
    print(f"⏱️  Time Span: {(datetime.fromisoformat(SAMPLE_MQTT_DATA[-1]['timestamp']) - datetime.fromisoformat(SAMPLE_MQTT_DATA[0]['timestamp'])).total_seconds()/3600:.1f} hours")
    print(f"🎯 Device: {SAMPLE_MQTT_DATA[0]['device']['name']}")
    print()

if __name__ == "__main__":
    print_mqtt_data()
