# MQTT Integration Testing Guide

## ✅ Status: Configuration Complete

Your app is now configured with **server-side MQTT integration**. Here's what's set up:

### Setup Summary
- **MQTT Data Source**: 192.168.1.10:1883 (ID: 1)
- **Test Device**: xiao_001 "Test Device (MQTT)" (ID: 1)
- **Admin User**: admin / admin123 (for login if needed)
- **Database**: SQLite pm_monitoring.db

---

## 🧪 Testing Approaches

### Approach 1: Browser-Side MQTT (Best for Local Testing)
Since 192.168.1.10 doesn't exist in this environment, the browser-side MQTT fallback is ideal.

**Steps:**
1. Open dashboard at `http://localhost:5000`
2. Login with `admin` / `admin123`
3. Open Browser DevTools Console (F12 → Console)
4. Run:
   ```javascript
   // Set to use public HiveMQ broker (no credentials needed)
   updateMQTTConfig(
     'wss://broker.hivemq.com:8884/mqtt',
     'xiao/dashboard',
     '',
     ''
   );
   ```
5. Verify output:
   ```
   ✅ MQTT browser client connected
   📡 Subscribed to MQTT topic: xiao/dashboard
   ```
6. In a **separate terminal**, publish test data:
   ```bash
   python mqtt_publisher.py
   ```
7. **Expected result**: Chart updates in real-time with incoming PM2.5, temperature, humidity data

**What you'll see:**
- Console: `📡 MQTT message received on xiao/dashboard`
- Console: `✅ Parsed MQTT data: {device_id: 'xiao_001', sensor: {...}, extended: {...}}`
- Dashboard: Charts animating with live data

---

### Approach 2: Server-Side MQTT (Production Ready)
For production, replace the broker IP with your actual MQTT broker:

**Update broker in database:**
```python
# Edit app.py line ~730 or update database:
# INSERT into dust_data_sources WHERE id=1:
# broker_url = 'broker.example.com'  (must support MQTT over TCP)
```

**Flow:**
- MQTT Device → Broker → Server (app.py MQTT client) → Database → WebSocket → Dashboard

---

## 📊 Real-Time Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    MQTT DEVICE                               │
│             (e.g., XIAO Sensor Board)                       │
│  Publishes: {"i":"xiao_001", "e":[...], "pm":[...]}        │
└────────────────────────┬────────────────────────────────────┘
                         │
                    MQTT Message
                         │
        ┌────────────────┴──────────────────┐
        │                                   │
        ▼                                   ▼
┌──────────────────┐             ┌──────────────────────┐
│ Browser-Side MQTT│             │ Server-Side MQTT    │
│  (Fallback)      │             │ (Recommended)        │
│                  │             │                      │
│ mqtt.connect()   │             │ paho.mqtt.client     │
│ → Dashboard      │             │ → SQLite DB          │
│   (real-time)    │             │ → Socket.IO/WS       │
│                  │             │ → Dashboard          │
└──────────────────┘             └──────────────────────┘
```

---

## 📨 MQTT Message Format (Compact)

The system supports three formats, but **compact is recommended**:

```json
{
  "i": "xiao_001",
  "e": [22.5, 45.3, 1013.25, 2.5, 750.0, 125.4, 45.2, 65.3],
  "pm": [12.5, 28.3, 35.1, 42.8, 50.0],
  "g": [51.5074, -0.1278, 45.2, 0.0],
  "t": "2024-01-01T12:00:00Z"
}
```

**Field Mapping:**
- `i`: Device ID (can also use `deviceid`)
- `e`: Environmental array `[temp°C, humidity%, pressure_hPa, UV_index, lux, VOC_ppb, NO2_ppb, noise_dB]`
- `pm`: PM array `[PM1, PM2.5, PM4, PM10, TSP_um]` (µg/m³)
- `g`: GPS array `[latitude, longitude, altitude_m, speed_kmh]`
- `t`: ISO timestamp

---

## 🚀 Quick Testing Commands

**Terminal 1** (already running):
```bash
# Flask app is running at http://localhost:5000
python app.py
```

**Terminal 2** (new - publish test data):
```bash
# Continuous publishing to public broker (10-second interval)
python mqtt_publisher.py

# OR single message with custom values
python mqtt_publisher.py custom xiao_001 35.0 23.5
```

**Terminal 3** (optional - subscribe and monitor):
```bash
# Subscribe to topic and see messages (requires mosquitto-clients installed)
mosquitto_sub -h broker.hivemq.com -p 8883 -t "xiao/dashboard" --cafile /etc/ssl/certs/ca-certificates.crt
```

---

## ✨ Live Dashboard Demo

### Login
- URL: `http://localhost:5000`
- Username: `admin`
- Password: `admin123`

### View Real-Time Data
1. Select device: "Test Device (MQTT)"
2. Charts will update every time a message arrives
3. Open DevTools (F12) to see console logs

### Example Console Output
```
✅ Socket.IO connection failed, trying MQTT...
✅ MQTT browser client connected
📡 Subscribed to MQTT topic: xiao/dashboard
📨 MQTT message received on xiao/dashboard
✅ Parsed MQTT data: {
  device_id: 'xiao_001',
  sensor: {
    timestamp: '2024-01-01T12:00:00.000Z',
    pm1: 12.5,
    pm2_5: 28.3,
    pm4: 35.1,
    pm10: 42.8,
    tsp: 50.0
  },
  extended: {
    temperature_c: 22.5,
    humidity_percent: 45.3,
    pressure_hpa: 1013.25,
    ...
  }
}
Processing incoming data: {...}
✅ WebSocket data processed successfully
```

---

## 🔧 Troubleshooting

### "MQTT client not initialized" in console
- Check: Is mqtt.js library loaded? (Should see `<script src="...mqtt.min.js">`)
- Check: Is browser connecting to public broker successfully?
- **Fix**: Try browser console: `updateMQTTConfig('wss://broker.hivemq.com:8884/mqtt', 'xiao/dashboard', '', '')`

### Server-side MQTT not connecting
- **Reason**: 192.168.1.10 is a private IP and not reachable in this environment
- **Fix**: Either:
  1. Use browser-side MQTT (no server changes needed)
  2. Update database `dust_data_sources` with a public broker or your actual broker IP

### Charts not updating
1. Check device is selected in dropdown
2. Open DevTools → Console, should see MQTT message logs
3. Verify data is matching the current device ID
4. Check `processIncomingData()` is being called

---

## 📝 Expected Output Sequence

```
1. Browser loads → Socket.IO tries to connect
2. Socket.IO fails → Fallback to MQTT
3. MQTT connects successfully
4. Browser publishes data to MQTT topic
5. MQTT message received by browser client
6. Data parsed and passed to dashboard
7. Charts update in real-time
8. Readings card shows latest PM values
9. Console logs show all operations
```

---

## 🎯 Next Steps

1. **Test browser MQTT** (now):
   - Open dashboard
   - Run `python mqtt_publisher.py`
   - Watch charts update in real-time

2. **Move to production** (when ready):
   - Configure real MQTT broker IP in database
   - Ensure broker supports MQTT over TCP (not WebSocket)
   - Server-side MQTT threads will handle ingestion automatically

3. **Customize** (optional):
   - Add more devices to `dust_devices` table
   - Configure threshold alerts in device settings
   - Enable relay control for devices with `has_relay=1`

---

**Happy testing!** 🚀
