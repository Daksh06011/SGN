# 🎯 MQTTX Integration Guide - Complete Setup

## What is MQTTX?

**MQTTX** is a user-friendly MQTT client tool that lets you:
- ✅ Connect to MQTT brokers (public or private)
- ✅ Subscribe to topics and receive messages
- ✅ Publish test data with a single click
- ✅ Monitor real-time message flow
- ✅ Test dashboard without writing code

**Available as:**
- Desktop GUI (recommended for beginners)
- Command-line tool
- Web version

---

## 📥 Installation

### **Option 1: Desktop Application (Easiest)**

1. **Visit**: https://mqttx.app/
2. **Download** for your OS:
   - Windows (installer or portable)
   - macOS
   - Linux

3. **Install** and launch the app

### **Option 2: Command-Line (CLI)**

```powershell
# Using npm (requires Node.js)
npm install -g mqtt-cli

# Or download pre-built binary from:
# https://github.com/emqx/MQTTX/releases
```

### **Option 3: Web Version (No Install)**

Visit: **https://mqtt-client-tools.emqxcloud.com/**

---

## 🚀 Quick Start (5 Minutes)

### **Step 1: Open MQTTX Desktop App**

Launch the application - you'll see the main interface

### **Step 2: Create New Connection**

Click **"New Connection"** (+ button in top-left)

Fill in these details:
```
┌─────────────────────────────────────┐
│  Connection Name: HiveMQ Public     │
│  Protocol:        mqtt              │
│  Host:            broker.hivemq.com │
│  Port:            1883              │
│  Username:        (leave empty)     │
│  Password:        (leave empty)     │
│  Client ID:       mqttx-dashboard   │
│  Keep Alive:      60                │
└─────────────────────────────────────┘
```

Click **"Connect"** button

**Expected:** ✅ Connected (green status indicator)

---

### **Step 3: Subscribe to Dashboard Topic**

In the left panel, click **"New Subscription"** (+ button)

Enter:
```
Topic: xiao/dashboard
QoS:   1
```

Click **"Subscribe"**

**Expected:** Topic appears in subscription list with "Connected" status

---

### **Step 4: Prepare Test Payload**

In the center/bottom section labeled **"Publish"**:

1. **Topic field:** `xiao/dashboard`
2. **QoS:** `1`
3. **Payload:** (see below for examples)

---

### **Step 5: Send First Message**

**Paste this compact format payload:**

```json
{
  "i": "xiao_001",
  "e": [22.5, 45.3, 1013.25, 2.5, 750.0, 125.4, 45.2, 65.3],
  "pm": [12.5, 28.3, 35.1, 42.8, 50.0],
  "g": [51.5074, -0.1278, 45.2, 0.0],
  "t": "2026-05-12T16:43:00Z"
}
```

Click **"Publish"**

**In MQTTX:** You'll see message appear in subscription window ✅

**In Dashboard (DevTools Console):**
```
📨 MQTT message received on xiao/dashboard
✅ Parsed MQTT data: {device_id: 'xiao_001', sensor: {...}, extended: {...}}
```

---

## 📊 Test Data Payloads

### **Format 1: Compact (Recommended)**

```json
{
  "i": "xiao_001",
  "e": [22.5, 45.3, 1013.25, 2.5, 750.0, 125.4, 45.2, 65.3],
  "pm": [12.5, 28.3, 35.1, 42.8, 50.0],
  "g": [51.5074, -0.1278, 45.2, 0.0],
  "t": "2026-05-12T16:43:00Z"
}
```

**Field Meanings:**
- `i` = Device ID
- `e` = Environmental [temp, humidity, pressure, uv, lux, voc, no2, noise]
- `pm` = Particulates [pm1, pm2.5, pm4, pm10, tsp]
- `g` = GPS [latitude, longitude, altitude, speed]
- `t` = Timestamp

---

### **Format 2: Extended**

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

---

### **Format 3: Simple**

```json
{
  "deviceid": "xiao_001",
  "pm1": 12.5,
  "pm2_5": 28.3,
  "pm4": 35.1,
  "pm10": 42.8,
  "tsp": 50.0
}
```

---

## 🎨 Test Scenarios

### **Scenario 1: Low Air Quality**

```json
{
  "i": "xiao_001",
  "e": [28.0, 65.0, 1012.0, 4.0, 600.0, 200.0, 80.0, 75.0],
  "pm": [40.0, 95.5, 120.0, 180.0, 250.0],
  "g": [51.5074, -0.1278, 45.2, 0.0],
  "t": "2026-05-12T16:43:00Z"
}
```

**Dashboard:** Shows HIGH PM2.5 ⚠️, red indicators

### **Scenario 2: Good Air Quality**

```json
{
  "i": "xiao_001",
  "e": [20.0, 35.0, 1015.0, 1.5, 1000.0, 50.0, 10.0, 45.0],
  "pm": [3.0, 8.0, 12.0, 18.0, 25.0],
  "g": [51.5074, -0.1278, 45.2, 0.0],
  "t": "2026-05-12T16:44:00Z"
}
```

**Dashboard:** Shows LOW PM2.5 ✅, green indicators

### **Scenario 3: Temperature Rising**

```json
{
  "i": "xiao_001",
  "e": [35.0, 50.0, 1010.0, 5.0, 800.0, 150.0, 50.0, 70.0],
  "pm": [20.0, 45.0, 60.0, 80.0, 100.0],
  "g": [51.5074, -0.1278, 45.2, 0.0],
  "t": "2026-05-12T16:45:00Z"
}
```

**Dashboard:** Temperature chart rises, humidity drops

---

## 🔄 Workflow: Testing with MQTTX

### **Manual Testing**

1. **Open MQTTX** → Connected to HiveMQ
2. **Subscribed** to `xiao/dashboard`
3. **Copy payload** from examples above
4. **Paste** into Publish message box
5. **Click Publish** ✅
6. **Watch** subscription window confirm receipt
7. **Switch to browser** → See charts update

### **Repeated Testing**

Create **saved messages** in MQTTX:
1. Click **"Saved"** tab in publish section
2. Create custom payloads
3. Name them (e.g., "Low Air Quality", "High Temp")
4. Click to publish anytime

---

## 🌐 Using MQTTX CLI

### **Installation**

```powershell
npm install -g mqtt-cli
```

### **Connect to Broker**

```powershell
# Subscribe to topic
mqtt-cli sub -h broker.hivemq.com -t xiao/dashboard -v
```

### **Publish Message**

```powershell
# In another terminal
mqtt-cli pub -h broker.hivemq.com -t xiao/dashboard -m '{"i":"xiao_001","pm":[12.5,28.3,35.1,42.8,50.0]}'
```

---

## 🌐 Using MQTTX Web Client

1. **Visit**: https://mqtt-client-tools.emqxcloud.com/
2. **No installation needed**
3. **Same steps** as desktop app
4. **Perfect for quick testing**

---

## 📱 Browser Dashboard Integration

### **Setup Browser**

1. **Open browser** at `http://localhost:5000`
2. **Login:** admin / admin123
3. **Select device:** XIAO Sensor Node (xiao_001)
4. **Open DevTools:** F12 → Console tab

### **Expected Console Output**

When you publish from MQTTX:

```
✅ MQTT browser client connected
📡 Subscribed to MQTT topic: xiao/dashboard
📨 MQTT message received on xiao/dashboard
✅ Parsed MQTT data: {
  device_id: 'xiao_001',
  sensor: {
    pm1: 12.5,
    pm2_5: 28.3,
    pm4: 35.1,
    pm10: 42.8,
    tsp: 50.0,
    timestamp: '2026-05-12T16:43:00Z'
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

**Dashboard:** Charts update with new PM2.5, temperature values ✨

---

## ✅ Verification Checklist

- [ ] MQTTX installed and running
- [ ] Connected to broker.hivemq.com:1883
- [ ] Subscribed to xiao/dashboard topic
- [ ] Browser dashboard loaded at localhost:5000
- [ ] Device "XIAO Sensor Node" selected
- [ ] DevTools console open and visible
- [ ] Test payload ready to paste
- [ ] Ready to publish and watch updates

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| MQTTX can't connect | Broker must be `broker.hivemq.com:1883` (no TLS for plain MQTT) |
| No messages in subscription | Check topic is exactly `xiao/dashboard` |
| Dashboard not updating | Verify device is selected, check browser console for errors |
| JSON parse error in console | Ensure payload is valid JSON (use jsonlint.com to verify) |
| Charts showing "--" | Payload missing "pm" field, use compact format example |

---

## 🚀 Next Steps

1. **Download MQTTX** from https://mqttx.app/
2. **Follow Quick Start** above (5 minutes)
3. **Test with provided payloads**
4. **Verify dashboard updates**
5. **Create custom payloads** for your scenarios

---

## 📞 Reference

**Public Broker Used:**
- Host: `broker.hivemq.com`
- Port: `1883`
- Protocol: `mqtt` (not TLS)
- No authentication required

**Dashboard:**
- URL: `http://localhost:5000`
- Credentials: admin / admin123
- Device: xiao_001 (XIAO Sensor Node)

**Topic:**
- Topic: `xiao/dashboard`
- QoS: 1
- Retention: No

---

**Ready to test real-time MQTT with MQTTX?** 🚀

Start with the Quick Start section above - you'll see live data in your dashboard in seconds!
