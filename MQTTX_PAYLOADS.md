# MQTTX Payload Reference Card

Use this file to quickly copy-paste test payloads into MQTTX!

## Connection Settings (Paste in MQTTX New Connection)
```
Broker:     broker.hivemq.com
Port:       1883
Protocol:   mqtt
Client ID:  mqttx-dashboard-test
Topic:      xiao/dashboard
QoS:        1
```

---

## Basic/Compact Format (Recommended)

### Normal Values
```json
{"i":"xiao_001","e":[22.5,45.3,1013.25,2.5,750.0,125.4,45.2,65.3],"pm":[12.5,28.3,35.1,42.8,50.0],"g":[51.5074,-0.1278,45.2,0.0],"t":"2026-05-12T16:43:00Z"}
```

### High Pollution
```json
{"i":"xiao_001","e":[28.0,65.0,1012.0,4.0,600.0,200.0,80.0,75.0],"pm":[40.0,95.5,120.0,180.0,250.0],"g":[51.5074,-0.1278,45.2,0.0],"t":"2026-05-12T16:43:00Z"}
```

### Clean Air
```json
{"i":"xiao_001","e":[20.0,35.0,1015.0,1.5,1000.0,50.0,10.0,45.0],"pm":[3.0,8.0,12.0,18.0,25.0],"g":[51.5074,-0.1278,45.2,0.0],"t":"2026-05-12T16:44:00Z"}
```

### Hot & Humid
```json
{"i":"xiao_001","e":[35.0,70.0,1010.0,5.5,500.0,180.0,70.0,75.0],"pm":[25.0,50.0,65.0,90.0,120.0],"g":[51.5074,-0.1278,45.2,0.0],"t":"2026-05-12T16:45:00Z"}
```

### Cold & Dry
```json
{"i":"xiao_001","e":[5.0,20.0,1020.0,0.5,1200.0,30.0,5.0,40.0],"pm":[2.0,5.0,8.0,12.0,18.0],"g":[51.5074,-0.1278,45.2,0.0],"t":"2026-05-12T16:46:00Z"}
```

---

## Extended Format (Alternative)

### Standard Data
```json
{
  "deviceid": "xiao_001",
  "Temperature_C": 23.5,
  "Humidity_%": 48.0,
  "Pressure_hPa": 1013.5,
  "UV_Index": 2.5,
  "Lux": 750.0,
  "VOC_ppb": 130.0,
  "NO2_ppb": 45.0,
  "Noise_dB": 65.0,
  "PM_data": {
    "PM1": 15.0,
    "PM2_5": 32.0,
    "PM4": 40.0,
    "PM10": 50.0,
    "TSP": 60.0
  },
  "GPS": {
    "Latitude": 51.5074,
    "Longitude": -0.1278,
    "Altitude_m": 45.2,
    "Speed_kmh": 0.0
  }
}
```

### High Pollution Extended
```json
{
  "deviceid": "xiao_001",
  "Temperature_C": 28.0,
  "Humidity_%": 65.0,
  "Pressure_hPa": 1012.0,
  "UV_Index": 4.0,
  "Lux": 600.0,
  "VOC_ppb": 200.0,
  "NO2_ppb": 80.0,
  "Noise_dB": 75.0,
  "PM_data": {
    "PM1": 40.0,
    "PM2_5": 95.5,
    "PM4": 120.0,
    "PM10": 180.0,
    "TSP": 250.0
  },
  "GPS": {
    "Latitude": 51.5074,
    "Longitude": -0.1278,
    "Altitude_m": 45.2,
    "Speed_kmh": 5.0
  }
}
```

---

## Simple Format (PM Only)

### Just PM Data
```json
{"deviceid":"xiao_001","pm1":12.5,"pm2_5":28.3,"pm4":35.1,"pm10":42.8,"tsp":50.0}
```

### High PM
```json
{"deviceid":"xiao_001","pm1":40.0,"pm2_5":95.5,"pm4":120.0,"pm10":180.0,"tsp":250.0}
```

### Low PM
```json
{"deviceid":"xiao_001","pm1":3.0,"pm2_5":8.0,"pm4":12.0,"pm10":18.0,"tsp":25.0}
```

---

## Field Reference

**Compact Format Fields:**
- `i` = Device ID (string)
- `e[0]` = Temperature (°C)
- `e[1]` = Humidity (%)
- `e[2]` = Pressure (hPa)
- `e[3]` = UV Index (0-16)
- `e[4]` = Lux (light level, 0-50000)
- `e[5]` = VOC (ppb, 0-500)
- `e[6]` = NO2 (ppb, 0-200)
- `e[7]` = Noise (dB, 30-100)
- `pm[0]` = PM1 (µg/m³)
- `pm[1]` = PM2.5 (µg/m³)
- `pm[2]` = PM4 (µg/m³)
- `pm[3]` = PM10 (µg/m³)
- `pm[4]` = TSP (µg/m³)
- `g[0]` = Latitude (degrees)
- `g[1]` = Longitude (degrees)
- `g[2]` = Altitude (meters)
- `g[3]` = Speed (km/h)
- `t` = Timestamp (ISO 8601)

**Typical Ranges:**
- Temperature: -10 to 50°C
- Humidity: 0-100%
- Pressure: 950-1050 hPa
- PM2.5 (Good): 0-35 µg/m³
- PM2.5 (Moderate): 35-75 µg/m³
- PM2.5 (Unhealthy): 75+ µg/m³

---

## MQTTX CLI Commands

```powershell
# Install
npm install -g mqtt-cli

# Subscribe (watch incoming messages)
mqtt-cli sub -h broker.hivemq.com -t xiao/dashboard

# Publish single message
mqtt-cli pub -h broker.hivemq.com -t xiao/dashboard -m '{"i":"xiao_001","pm":[12.5,28.3,35.1,42.8,50.0]}'

# Publish from file
mqtt-cli pub -h broker.hivemq.com -t xiao/dashboard -m "$(cat payload.json)"
```

---

## Quick Testing Steps

1. **In MQTTX Desktop:**
   - New Connection → broker.hivemq.com:1883
   - New Subscription → xiao/dashboard
   - Publish section → paste payload above
   - Click "Publish"

2. **In Browser:**
   - Open http://localhost:5000
   - DevTools Console (F12)
   - Should see: "MQTT message received"
   - Charts update with data ✨

3. **Try different payloads** from above to see:
   - ✅ Charts update
   - ✅ PM values change
   - ✅ Temperature/humidity respond
   - ✅ Readings card updates

---

**Copy any payload → Paste in MQTTX → Click Publish → Watch Dashboard Update!** 🚀
