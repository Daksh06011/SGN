# 🚀 MQTT Integration: Complete Setup & Testing Summary

## ✅ What's Been Done

### 1. **Added MQTT Script to Dashboard** (`templates/dashboard.html`)
   ```html
   <script src="https://cdn.socket.io/4.7.4/socket.io.min.js"></script>
   <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script> ← NEW
   ```

### 2. **Added Browser-Side MQTT Client** (`static/script.js`)
   - **Lines 17-25**: MQTT configuration (broker, topic, credentials)
   - **Lines 29-95**: MQTT payload parser (handles 3 formats: compact, extended, simple)
   - **Lines 100-180**: MQTT client initialization and connection handlers
   - **Lines 372, 388-393**: Fallback logic when Socket.IO fails
   - **Functions added**:
     - `parseMQTTPayload()`: Parse incoming MQTT messages
     - `initializeMQTTClient()`: Connect to MQTT broker
     - `disconnectMQTTClient()`: Clean shutdown
     - `updateMQTTConfig()`: Change broker settings at runtime

### 3. **Set Up Database for MQTT** (SQLite: `pm_monitoring.db`)
   - ✅ MQTT Data Source: `dust_data_sources` (ID=1, Broker: 192.168.1.10)
   - ✅ Test Device: `dust_devices` (ID=1, Device ID: xiao_001)
   - ✅ Admin User: `dust_users` (username: admin, password: admin123)

### 4. **Flask App Ready** (Running on `http://localhost:5000`)
   - ✅ Database initialization ✓
   - ✅ MQTT client threads spawned ✓
   - ✅ WebSocket (Socket.IO) server running ✓
   - ℹ️  Server-side MQTT threads trying 192.168.1.10 (expected to fail - private IP)

### 5. **Test Data Publisher Ready** (`mqtt_publisher.py`)
   - Updated to use public broker: `broker.hivemq.com:8883`
   - Publishes compact MQTT format data
   - Auto-reconnect with 15-second retry

---

## 🎯 Testing Flow: Step-by-Step

### **Step 1: Start Flask Application** ✅ (DONE)
```bash
python app.py
# App running on http://localhost:5000
# MQTT threads initialized (failing gracefully on private IP)
```

**Expected Terminal Output:**
```
INFO:__main__:[STARTUP] ✨ Railway Flask app ready!
INFO:werkzeug: * Running on http://0.0.0.0:5000
```

---

### **Step 2: Publish Test Data** (New Terminal)
```bash
python mqtt_publisher.py
```

**What it does:**
- Connects to public HiveMQ broker (broker.hivemq.com:8883)
- Publishes compact MQTT messages to topic: `xiao/dashboard`
- Sends data every 10 seconds indefinitely
- Example message:
  ```json
  {
    "i": "xiao_001",
    "e": [22.5, 45.3, 1013.25, 2.5, 750.0, 125.4, 45.2, 65.3],
    "pm": [12.5, 28.3, 35.1, 42.8, 50.0],
    "g": [51.5074, -0.1278, 45.2, 0.0],
    "t": "2024-01-01T12:00:00Z"
  }
  ```

---

### **Step 3: Open Dashboard** (Browser)
```
URL: http://localhost:5000
Username: admin
Password: admin123
```

**Steps:**
1. Open DevTools (F12 → Console tab)
2. Select Device: "Test Device (MQTT)" from dropdown
3. Watch the console for MQTT connection logs
4. Charts should update in real-time

---

### **Step 4: Verify Connection** (Browser Console)
Paste this in DevTools Console to test:
```javascript
// Set to use public HiveMQ broker
updateMQTTConfig(
  'wss://broker.hivemq.com:8884/mqtt',
  'xiao/dashboard',
  '',
  ''
);
```

**Expected Console Output:**
```
🔌 Initializing MQTT browser client...
   Broker: wss://broker.hivemq.com:8884/mqtt
   Topic: xiao/dashboard
✅ MQTT browser client connected
📡 Subscribed to MQTT topic: xiao/dashboard
📨 MQTT message received on xiao/dashboard
✅ Parsed MQTT data: {device_id: 'xiao_001', sensor: {...}, extended: {...}}
```

---

## 📊 Real-Time Update Flow

```
MQTT Publisher (mqtt_publisher.py)
         ↓
    [every 10 sec]
         ↓
Public HiveMQ Broker
  (broker.hivemq.com:8883)
         ↓
   [MQTT over WSS]
         ↓
Browser MQTT Client (mqtt.js)
  ↓
Parse Message (parseMQTTPayload)
  ↓
Update Dashboard (processIncomingData)
  ↓
Charts Update in Real-Time ✨
```

---

## 🔧 Three Ways to Test

### **Option A: Browser-Side MQTT (Easiest - Recommended)**
- ✅ Works immediately with public broker
- ✅ No broker setup required
- ✅ Fallback when server unavailable
- Browser connects directly to: `wss://broker.hivemq.com:8884/mqtt`

**Test:**
```bash
Terminal 1: python app.py
Terminal 2: python mqtt_publisher.py
Browser: http://localhost:5000
```

---

### **Option B: Server-Side MQTT (Production)**
- ✅ Data stored in database
- ✅ Threshold alerts enabled
- ✅ Better security & reliability
- Requires real MQTT broker with TCP support (not WebSocket)

**Setup:**
```sql
-- Update database with your broker
UPDATE dust_data_sources 
SET broker_url = 'your-broker.com' 
WHERE id = 1;
```

**Flow**: Device → Broker → Server → DB → WebSocket → Dashboard

---

### **Option C: Direct Server Publishing (Testing)**
```bash
# Simulate device publishing to server-side MQTT
python mqtt_publisher.py custom xiao_001 35.0 23.5
```

---

## 📈 Data Formats Supported

### **Compact Format** (Recommended)
```json
{
  "i": "xiao_001",
  "e": [temp, humid, press, uv, lux, voc, no2, noise],
  "pm": [pm1, pm2.5, pm4, pm10, tsp],
  "g": [lat, lon, alt, speed],
  "t": "ISO_timestamp"
}
```

### **Extended Format**
```json
{
  "deviceid": "xiao_001",
  "Temperature_C": 22.5,
  "Humidity_%": 45.3,
  "PM_data": {"PM1": 12.5, "PM2_5": 28.3, ...},
  "GPS": {"Latitude": 51.5074, ...}
}
```

### **Simple Format**
```json
{
  "deviceid": "xiao_001",
  "pm1": 12.5,
  "pm2_5": 28.3,
  ...
}
```

---

## ✨ Expected Dashboard Behavior

### **Before Device Selection**
```
"Dashboard initialized. Please select a device to load data."
```

### **After Selecting "Test Device (MQTT)"**
1. Device info panel shows: "Online" (if data received)
2. Charts appear with history data
3. Real-time readings update every 10 seconds
4. Console shows:
   ```
   📡 Received WebSocket sensor data
   ✅ WebSocket data processed successfully
   ✔ Device selected: xiao_001 (Type: basic)
   ```

### **Live Updates**
- **PM1, PM2.5, PM4, PM10, TSP** values refresh
- **Quick stats** show device count, online status, alerts
- **Last Update** time changes
- **Charts** animate new data points

---

## 🐛 Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| "MQTT not found" in console | mqtt.js not loaded | Check `<script src="mqtt.min.js">` in dashboard.html |
| Charts not updating | Device ID mismatch | Verify device ID in MQTT message = "xiao_001" |
| "No address found" in server logs | Broker IP invalid | Update `dust_data_sources.broker_url` or use public broker |
| No console logs | Socket.IO not available | Check browser MQTT fallback activation |
| Browser MQTT won't connect | WSS protocol issue | Try `wss://` broker URL, not `ws://` |
| Unicode error in publisher | Windows encoding | Publisher now fixed with UTF-8 encoding |

---

## 📋 Verification Checklist

- [x] MQTT library added to HTML
- [x] MQTT client code in script.js
- [x] Database configured (MQTT source, test device)
- [x] Flask app running
- [x] Publisher configured for public broker
- [x] Device selection working
- [ ] Real-time updates working (TO TEST)
- [ ] Charts updating with live data (TO TEST)

---

## 🚀 Production Deployment

When ready for production:

1. **Use Real MQTT Broker**
   ```sql
   UPDATE dust_data_sources 
   SET broker_url = 'your-enterprise-broker.com'
   WHERE id = 1;
   ```

2. **Configure Credentials** (if needed)
   ```sql
   UPDATE dust_data_sources 
   SET username = 'user', password = 'pass'
   WHERE id = 1;
   ```

3. **Enable Threshold Alerts**
   - Set `has_relay = 1` for devices with control relays
   - Configure thresholds in device settings

4. **Monitor Server Logs**
   - MQTT connection status
   - Message parsing errors
   - Database insert operations

---

## 📞 Support

### Quick Test Command
```bash
# Terminal 1
python app.py

# Terminal 2
python mqtt_publisher.py

# Terminal 3 (optional - monitor messages)
# Use mosquitto_sub or web MQTT client:
# mqtt-explorer.io (web-based MQTT client)
```

### Debug Logs
**Server**: Check terminal running `python app.py` for MQTT logs
**Browser**: Open DevTools Console (F12) to see client-side logs
**Publisher**: Should show connection status and message publish confirmations

---

**Status: READY FOR TESTING** ✨

Next: Open browser, select device, and watch real-time data flow!
