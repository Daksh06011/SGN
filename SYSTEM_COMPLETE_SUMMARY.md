# 🌍 Complete AQI Monitoring System - Implementation Summary

## 📡 System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      SENSOR DEVICES                             │
│                    (xiao-cam-01, etc.)                          │
│              └─ PM1.0, PM2.5, PM4.0, PM10                       │
│              └─ Temperature, Humidity, Signal Strength           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MQTT BROKER                                  │
│              (Receives JSON sensor payloads)                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              FLASK BACKEND (app.py)                             │
├─────────────────────────────────────────────────────────────────┤
│  ✓ Payload parsing & validation                                │
│  ✓ Device authorization check                                  │
│  ✓ AQI Calculation (UK DAQI Formula)                           │
│  ✓ Database insertion (SQLite/PostgreSQL)                      │
│  ✓ WebSocket emission (real-time updates)                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
    DATABASE                        WEBSOCKET
    (SQLite)                        (Socket.IO)
    ┌──────────────┐               ┌──────────────┐
    │ Sensor Data  │               │ Live Client  │
    │ Extended Data│               │ (Browser)    │
    └──────────────┘               └──────────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │  FRONTEND (Dashboard)│
                              │  - HTML Templates   │
                              │  - JavaScript Logic │
                              │  - CSS Styling      │
                              └──────────────────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │  USER INTERFACE      │
                              │  - Charts & Graphs   │
                              │  - AQI Display       │
                              │  - Real-time Metrics │
                              └──────────────────────┘
```

---

## 🧮 AQI Calculation Logic

### UK DAQI Formula Implementation

```python
def calculate_aqi(pm2_5, pm10):
    """
    Calculate UK Daily Air Quality Index (DAQI)
    Based on PM2.5 and PM10 thresholds
    """
    
    # Classification table
    if pm2_5 <= 11.0 and pm10 <= 40.0:
        return {
            'index': 0,
            'level': 'Low',
            'color': '#00AA00',  # Green
            'description': 'Air quality is good. Enjoy outdoor activities.'
        }
    elif pm2_5 <= 23.5 and pm10 <= 80.0:
        return {
            'index': 50,
            'level': 'Moderate',
            'color': '#FFFF00',  # Yellow
            'description': 'Air quality is acceptable. Most can engage in outdoor activities.'
        }
    elif pm2_5 <= 47.0 and pm10 <= 160.0:
        return {
            'index': 100,
            'level': 'High',
            'color': '#FF8800',  # Orange
            'description': 'Sensitive groups should limit outdoor activities.'
        }
    else:
        return {
            'index': 150,
            'level': 'Very High',
            'color': '#FF0000',  # Red
            'description': 'Everyone should avoid outdoor activities.'
        }
```

### Example: Your Data
```
Input:  PM2.5 = 7 µg/m³,  PM10 = 7 µg/m³
Check:  7 ≤ 11.0 ✓  AND  7 ≤ 40.0 ✓
Result: 🟢 LOW AQI (Index 0)
```

---

## 📊 Dashboard Layout & Display

### Top to Bottom Flow

```
╔════════════════════════════════════════════════════════════════════╗
║                    SGN CONTROLS V2.0                              ║
║                    Environmental Monitor                           ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  Quick Stats Row:                                                  ║
║  ┌──────────┬──────────┬──────────┬──────────┬──────────┬────────┐║
║  │ Devices  │ Online   │ Alerts   │ Avg PM   │ Max Temp │  AQI   ││
║  │    0     │    0     │    0     │   --     │  --°C    │   --   ││
║  └──────────┴──────────┴──────────┴──────────┴──────────┴────────┘║
║                                                                    ║
╠════════════════════════════════════════════════════════════════════╣
║  Temperature Section                                               ║
║  ┌────────────────────────────────────────────────────────────┐  ║
║  │ Live Temperature Data                                      │  ║
║  │ (--°C) Current temperature reading                         │  ║
║  └────────────────────────────────────────────────────────────┘  ║
║                                                                    ║
╠════════════════════════════════════════════════════════════════════╣
║  Device Selection & Data Export (Side-by-Side)                    ║
║  ┌─────────────────────────┬─────────────────────────────────┐  ║
║  │ Device Selection        │ Data Export                     │  ║
║  │ ─────────────────────   │ ─────────────────────           │  ║
║  │ Select Device: [▼]      │ From: [2026-05-10]              │  ║
║  │ [Refresh] [Auto]        │ To:   [2026-05-17]              │  ║
║  │                         │ [📥 Export CSV]                 │  ║
║  └─────────────────────────┴─────────────────────────────────┘  ║
║                                                                    ║
╠════════════════════════════════════════════════════════════════════╣
║  AIR QUALITY INDEX SECTION ⭐ (NEW POSITION)                      ║
║  ┌───────────────────────────────────────────────────────────┐  ║
║  │ 🏷 Air Quality    📊 UK DAQI Standard                      │  ║
║  │                                                           │  ║
║  │  ┌──────────┐  Current Status: --                        │  ║
║  │  │          │  No data available                         │  ║
║  │  │   AQI    │                                            │  ║
║  │  │   --     │  PM2.5: -- µg/m³    PM10: -- µg/m³         │  ║
║  │  │   AQI    │  15-min Avg: --                            │  ║
║  │  │          │                                            │  ║
║  │  └──────────┘                                            │  ║
║  │                                                           │  ║
║  │  AQI SCALE (UK DAQI)                                      │  ║
║  │  ┌─────────┬─────────────┬───────────┬──────────────┐    │  ║
║  │  │🟢 Low   │🟡 Moderate  │🟠 High    │🔴 Very High  │    │  ║
║  │  │ 0-50    │  50-100     │ 100-150   │  150+        │    │  ║
║  │  └─────────┴─────────────┴───────────┴──────────────┘    │  ║
║  └───────────────────────────────────────────────────────────┘  ║
║                                                                    ║
╠════════════════════════════════════════════════════════════════════╣
║  Enhanced Tabs (Charts, Overview, etc.)                           ║
║  [🎯 Overview]  [📊 Unified]  [Other Tabs...]                    ║
║  ┌─────────────────────────────────────────────────────────┐    ║
║  │ PM Levels Over Time (Chart)                             │    ║
║  │ Current PM Levels | Air Quality Index                   │    ║
║  └─────────────────────────────────────────────────────────┘    ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

---

## 🔄 Real-Time Data Flow

### WebSocket Message Format

```json
{
  "timestamp": "2026-05-15 14:05:00",
  "temperature": 30.2,
  "pm1": 7,
  "pm2_5": 7,
  "pm4": 7,
  "pm10": 7,
  "tsp": 7,
  "aqi": {
    "current": {
      "index": 0,
      "level": "Low",
      "color": "#00AA00",
      "description": "Air quality is good. Enjoy outdoor activities.",
      "range": "0-50"
    },
    "average": {
      "index": 0,
      "level": "Low"
    }
  }
}
```

### Frontend Processing Chain

```
socket.on('new_data') [WebSocket receives]
         ↓
updateAQI(data) [Main handler]
         ↓
updateAQIFromBackend(aqiData) [Display handler]
         ├─ Update #aqiIcon (color)
         ├─ Update #aqiIndex (number)
         ├─ Update #aqiLevel (text)
         ├─ Update #aqiCircle (border color)
         ├─ Update #aqiPM25Main (PM2.5 value)
         ├─ Update #aqiPM10Main (PM10 value)
         └─ Update #aqiAverageMain (15-min avg)
         ↓
Chart.update() [Add data point]
```

---

## 🎨 Color-Coded Status System

### Visual Indicators

| Status | Color | Hex | PM2.5 Range | PM10 Range | Icon |
|--------|-------|-----|------------|-----------|------|
| **Low** | 🟢 Green | #00AA00 | ≤ 11.0 | ≤ 40.0 | ✓ Safe |
| **Moderate** | 🟡 Yellow | #FFFF00 | ≤ 23.5 | ≤ 80.0 | ⚠ Caution |
| **High** | 🟠 Orange | #FF8800 | ≤ 47.0 | ≤ 160.0 | ⚠⚠ Alert |
| **Very High** | 🔴 Red | #FF0000 | > 47.0 | > 160.0 | ✗ Avoid |

### Visual Feedback

```
Status Display:
┌─ Circular Gauge ────────────┐
│                             │
│   Color Border (AQI Level)  │
│   Center Text (Index)       │
│   Label: "AQI"              │
│                             │
└─────────────────────────────┘

Additional Displays:
├─ Level Badge (text with level name)
├─ Description (health recommendation)
├─ PM Values (real-time readings)
├─ Average (15-min rolling average)
└─ Scale Legend (all 4 levels shown)
```

---

## 💾 Database Schema Integration

### dust_sensor_data Table
```
timestamp    TIMESTAMP     - Reading timestamp
device_id    INT           - Device identifier
data_source_id VARCHAR     - MQTT source
pm1          FLOAT         - PM1.0 (µg/m³)
pm2_5        FLOAT         - PM2.5 (µg/m³) ← Used for AQI
pm4          FLOAT         - PM4.0 (µg/m³)
pm10         FLOAT         - PM10 (µg/m³) ← Used for AQI
tsp          FLOAT         - Total Suspended Particles
```

### dust_extended_data Table
```
device_id         INT       - Device identifier
timestamp         TIMESTAMP - Reading timestamp
temperature_c     FLOAT     - Temperature
humidity_percent  FLOAT     - Humidity
voc_ppb          FLOAT     - Volatile Organic Compounds
no2_ppb          FLOAT     - Nitrogen Dioxide
noise_db         FLOAT     - Noise Level
pm1-pm10         FLOAT     - All particulate matter values
gps_lat/lon      FLOAT     - GPS coordinates
```

---

## 🧪 Example Output: Your Sensor Data

### Input
```json
{
  "site": "xiao-cam-01",
  "mac": "90:70:69:12:B9:CC",
  "tsi_pm25": 7,
  "tsi_pm10": 7,
  "tsi_temp": 30.2,
  "tsi_rh": 72
}
```

### Processing
```
Step 1: Parse JSON ✓
Step 2: Validate Device ✓
Step 3: Store in Database ✓
Step 4: Calculate AQI
        - Check PM2.5 (7) ≤ 11.0? YES
        - Check PM10 (7) ≤ 40.0? YES
        - Result: LOW ✓
Step 5: Send via WebSocket ✓
```

### Display Output
```
Quick Card:     AQI: 0 (Low)
Main Gauge:     🟢 Green border, "0" center
Status Text:    "Air quality is good. Enjoy outdoor activities."
PM Display:     PM2.5: 7 µg/m³ | PM10: 7 µg/m³
Average:        0 (Low)
Chart:          New data point added
```

---

## ✅ Implementation Checklist

- [x] UK DAQI formula implemented
- [x] Backend AQI calculation integrated
- [x] WebSocket real-time updates
- [x] Frontend HTML elements created
- [x] JavaScript update logic implemented
- [x] CSS styling and colors applied
- [x] Dashboard section repositioned (below Device Selection)
- [x] Color-coded status system
- [x] 15-minute rolling average tracking
- [x] Database schema compatibility
- [x] Error handling and fallbacks
- [x] Responsive layout design
- [x] Documentation and testing

---

## 🚀 Features Ready

- ✅ Real-time AQI monitoring
- ✅ Multi-device support
- ✅ Historical data tracking
- ✅ Automatic threshold detection
- ✅ Color-coded warnings
- ✅ CSV export with AQI values
- ✅ Mobile-responsive display
- ✅ Live chart updates
- ✅ Device selection and filtering
- ✅ Data analytics and trends

---

## 📈 Future Enhancements

- Predictive AQI forecasting
- Health recommendation alerts
- Comparative analysis between devices
- Weekly/monthly trend reports
- Map-based monitoring
- Mobile app integration
- Notification system
- Data archival strategy

---

**🎉 System Complete and Ready for Live Sensor Data!**
