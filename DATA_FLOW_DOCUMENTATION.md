# Data Flow: From Sensor to Dashboard Display

## 1. INCOMING SENSOR DATA (xiao-cam-01)
```json
{
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
  "tsi_temp": 30.2,
  "tsi_rh": 72
}
```

---

## 2. BACKEND PROCESSING (Flask/MQTT Handler)

### Data Reception
- **MQTT Broker** receives the JSON payload
- **on_message()** handler parses and validates the data
- Checks device authorization and data source ID

### Database Storage

#### dust_sensor_data table
```
timestamp     | 2026-05-15 14:05:00
device_id     | 1
pm1           | 7000
pm2_5         | 7000
pm4           | 7000
pm10          | 7000
tsp           | 7000
```

#### dust_extended_data table
```
device_id         | 1
timestamp         | 2026-05-15 14:05:00
temperature_c     | 30.2
humidity_percent  | 72
voc_ppb           | 0
no2_ppb           | 0
noise_db          | 0
pm1               | 7
pm2_5             | 7
pm4               | 7
pm10              | 7
gps_lat           | 0
gps_lon           | 0
```

### AQI Calculation (UK DAQI Formula)
```python
def calculate_aqi(pm2_5, pm10):
    if pm2_5 <= 11.0 and pm10 <= 40.0:
        return {
            'index': 0,
            'level': 'Low',
            'color': '#00AA00',
            'description': 'Air quality is good. Enjoy outdoor activities.'
        }
```

**Input:** PM2.5 = 7 µg/m³, PM10 = 7 µg/m³  
**Output:** AQI Level = **Low** (Index 0)

---

## 3. WEBSOCKET UPDATE TO FRONTEND

### emit_websocket_update() sends:
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

### socket.on('new_data') receives and triggers updateAQI()

---

## 4. FRONTEND DISPLAY

### Quick Stat Card (Header)
```
┌────────────┐
│     --     │  AQI
│   Metric   │
└────────────┘
```
- Updates dynamically with AQI index and level
- Color-coded background (green for Low, yellow for Moderate, orange for High, red for Very High)

### Comprehensive AQI Section (Below Device Selection)
```
┌────────────────────────────────────────────────────────┐
│                  AIR QUALITY INDEX                     │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌─────────────┐  ┌──────────────────────────────┐   │
│  │   AQI       │  │ Current Status: Low          │   │
│  │   Gauge     │  │ Good air quality             │   │
│  │   Color:    │  │                              │   │
│  │   #00AA00   │  │ PM2.5: 7 µg/m³              │   │
│  │             │  │ PM10: 7 µg/m³               │   │
│  │   (120px)   │  │ 15-min Avg: 0                │   │
│  └─────────────┘  └──────────────────────────────┘   │
│                                                        │
├────────────────────────────────────────────────────────┤
│  AQI SCALE (UK DAQI)                                   │
│  🟢 Low(0-50) 🟡 Moderate(50-100)                     │
│  🟠 High(100-150) 🔴 Very High(150+)                  │
└────────────────────────────────────────────────────────┘
```

### Connected Charts
- **PM Levels Over Time**: New data point added at timestamp
- **Legend**: PM1, PM2.5, PM4, PM10, TSP visualization
- **Real-time Updates**: All values update as WebSocket data arrives

---

## 5. REAL-TIME MONITORING

### Live Updates Every 1-2 Seconds
```
WebSocket Flow:
Device → MQTT Broker → Flask Backend → Database → WebSocket → Browser
   ↓                        ↓                          ↓
Data In              AQI Calculation            Visual Update
                    Data Storage               (Charts, Stats)
```

### 15-Minute Rolling Average
- System tracks last 15 minutes of readings
- Calculates average AQI level
- Displays in comprehensive AQI section
- Used for trend analysis

---

## 6. DISPLAY LOGIC (Frontend JavaScript)

### updateAQI() Function
```javascript
function updateAQI(data) {
    // Check for backend AQI data
    if (data.aqi && data.aqi.current) {
        updateAQIFromBackend(data.aqi);
    }
    
    // Update quick stat card
    document.getElementById('aqiIndex').textContent = aqi.current.index;
    document.getElementById('aqiLevel').textContent = aqi.current.level;
    
    // Update main AQI section
    document.getElementById('aqiCircle').style.borderColor = aqi.current.color;
    document.getElementById('aqiIndexMain').textContent = aqi.current.index;
    document.getElementById('aqiLevelMain').textContent = aqi.current.level;
    document.getElementById('aqiDescription').textContent = aqi.current.description;
    document.getElementById('aqiPM25Main').textContent = data.pm2_5.toFixed(1);
    document.getElementById('aqiPM10Main').textContent = data.pm10.toFixed(1);
    document.getElementById('aqiAverageMain').textContent = aqi.average.index;
}
```

---

## 7. DASHBOARD SECTION ORDER

1. **Header** with Quick Stat Cards (including AQI)
2. **Temperature Section** (Live temp from device)
3. **Device Selection & Data Export** (side by side)
4. **AQI Section** ← NOW POSITIONED HERE (Below Device Selection)
5. **Enhanced Tabs** (Overview, Charts, etc.)

---

## 8. COLOR CODING SYSTEM

| Level | Color | Range | Background | Status |
|-------|-------|-------|-----------|--------|
| Low | 🟢 #00AA00 | 0-50 | Green | Safe ✓ |
| Moderate | 🟡 #FFFF00 | 50-100 | Yellow | Caution ⚠ |
| High | 🟠 #FF8800 | 100-150 | Orange | Alert ⚠⚠ |
| Very High | 🔴 #FF0000 | 150+ | Red | Critical ✗ |

---

## 9. KEY METRICS DISPLAYED

```
Real-Time Readings:
├─ Current AQI Index (0-500)
├─ AQI Level (Low/Moderate/High/Very High)
├─ PM2.5 (µg/m³)
├─ PM10 (µg/m³)
├─ Temperature (°C)
├─ Humidity (%)
├─ 15-Minute Average AQI
└─ Status Description

Device Info:
├─ Device ID: xiao-cam-01
├─ MAC: 90:70:69:12:B9:CC
├─ Last Update: 2026-05-15 14:05:00
└─ Signal Strength: -69 dBm
```

---

## 10. EXAMPLE WITH YOUR DATA

**Input Sensor Values:**
- PM2.5: 7 µg/m³
- PM10: 7 µg/m³
- Temperature: 30.2°C
- Humidity: 72%

**Processing:**
1. ✓ Received and validated by Flask
2. ✓ Stored in database
3. ✓ AQI calculated (Low)
4. ✓ Sent via WebSocket

**Display:**
- Quick Card: **AQI: 0 (Low)**
- Main Section: 
  - Circular gauge with 🟢 green border
  - Status: "Air quality is good. Enjoy outdoor activities."
  - PM Values: 7 µg/m³, 7 µg/m³
  - 15-min Average: 0 (Low)

---

**✅ Complete data flow from sensor to beautiful dashboard display!**
