# 🚀 Quick Start: Real-Time MQTT Dashboard Testing

**Get the dashboard updating with live sensor data in 5 minutes!**

---

## ⚡ Fastest Method: Python Helper Script

### Step 1: Start Flask Server (Keep Running)
```powershell
cd c:\Users\daksh\Downloads\Compressed\uk_pm_monitoring-main\uk_pm_monitoring-main
python app.py
# Leave this running! Don't close the terminal
```

### Step 2: Open Dashboard in Browser
- Open: http://localhost:5000
- Login: admin / admin123
- Select device: "XIAO Sensor Node"
- Keep this open - you'll watch it update

### Step 3: Publish Test Data (New Terminal)
```powershell
# Open NEW PowerShell/Command terminal (don't close Flask terminal!)
cd c:\Users\daksh\Downloads\Compressed\uk_pm_monitoring-main\uk_pm_monitoring-main

# Try different scenarios:
python mqttx_helper.py normal       # Normal air quality
python mqttx_helper.py clean        # Clean air
python mqttx_helper.py polluted     # High pollution
python mqttx_helper.py hot          # Hot & humid
python mqttx_helper.py cold         # Cold & dry
```

### Step 4: Watch Dashboard Update ✨
- Check browser dashboard - charts update
- Check Console (F12) - see MQTT logs
- **Done!** You have real-time MQTT working!

---

## 🖥️ Alternative: MQTTX Desktop GUI

For a visual, GUI-based approach:

### Installation
1. Download: https://mqttx.app/
2. Install and launch MQTTX Desktop

### Connection
1. Click **"+ New Connection"**
2. Set these values:
   - Broker: `broker.hivemq.com`
   - Port: `1883`
   - Protocol: `mqtt`
   - Client ID: `mqttx-dashboard-test`
3. Click **"Connect"** (wait for ✅)

### Subscribe
1. Click **"+ New Subscription"**
2. Topic: `xiao/dashboard`
3. QoS: `1`
4. Click **"Subscribe"**

### Publish (Copy-Paste Ready!)
1. Scroll to **"Publish"** section
2. Set Topic: `xiao/dashboard`
3. Copy payload below and paste in message box:

**Compact Format (Recommended):**
```json
{"i":"xiao_001","e":[22.5,45.3,1013.25,2.5,750.0,125.4,45.2,65.3],"pm":[12.5,28.3,35.1,42.8,50.0],"g":[51.5074,-0.1278,45.2,0.0],"t":"2026-05-12T16:43:00Z"}
```

4. Click **"Publish"**
5. Watch browser dashboard update!

**More payloads?** See `MQTTX_PAYLOADS.md`

---

## 🧪 Test Scenarios (Copy-Paste in MQTTX)

### 📊 Normal Air Quality
```json
{"i":"xiao_001","e":[22.5,45.3,1013.25,2.5,750.0,125.4,45.2,65.3],"pm":[12.5,28.3,35.1,42.8,50.0],"g":[51.5074,-0.1278,45.2,0.0],"t":"2026-05-12T16:43:00Z"}
```

### ✨ Clean Air
```json
{"i":"xiao_001","e":[20.0,35.0,1015.0,1.5,1000.0,50.0,10.0,45.0],"pm":[3.0,8.0,12.0,18.0,25.0],"g":[51.5074,-0.1278,45.2,0.0],"t":"2026-05-12T16:44:00Z"}
```

### 🔴 High Pollution
```json
{"i":"xiao_001","e":[28.0,65.0,1012.0,4.0,600.0,200.0,80.0,75.0],"pm":[40.0,95.5,120.0,180.0,250.0],"g":[51.5074,-0.1278,45.2,0.0],"t":"2026-05-12T16:45:00Z"}
```

### 🔥 Hot & Humid
```json
{"i":"xiao_001","e":[35.0,70.0,1010.0,5.5,500.0,180.0,70.0,75.0],"pm":[25.0,50.0,65.0,90.0,120.0],"g":[51.5074,-0.1278,45.2,0.0],"t":"2026-05-12T16:46:00Z"}
```

### ❄️ Cold & Dry
```json
{"i":"xiao_001","e":[5.0,20.0,1020.0,0.5,1200.0,30.0,5.0,40.0],"pm":[2.0,5.0,8.0,12.0,18.0],"g":[51.5074,-0.1278,45.2,0.0],"t":"2026-05-12T16:47:00Z"}
```

---

## ✅ Verify It's Working

### In Browser Console (F12)
You should see logs like:
```
📨 MQTT message received on xiao/dashboard
✅ Parsed MQTT data: {device_id: 'xiao_001', sensor: {…}, extended: {…}}
```

### In Dashboard
- PM2.5 chart updates ✓
- Temperature value changes ✓
- Humidity refreshes ✓
- Readings card shows latest data ✓

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| "Flask not running" | Run `python app.py` first |
| Dashboard blank | Refresh browser, select device |
| No MQTT logs in console | Check browser console (F12) is open |
| "Connection refused" | Ensure Flask server is running |
| MQTTX won't connect | Verify internet, use broker.hivemq.com:1883 |
| Python script errors | Install: `pip install paho-mqtt` |

---

## 📁 Key Files Reference

- **Dashboard:** http://localhost:5000
- **Login:** admin / admin123
- **Device:** XIAO Sensor Node
- **Python helper:** `mqttx_helper.py`
- **Payloads:** `MQTTX_PAYLOADS.md`
- **Detailed guide:** `MQTTX_SETUP_GUIDE.md`

---

## 🎯 What's Happening?

```
Your Computer
    ↓
Python Script / MQTTX
    ↓
HiveMQ Public Broker (broker.hivemq.com)
    ↓
Browser JavaScript (MQTT.js)
    ↓
Real-Time Dashboard Update ✨
```

**The Flask server bridges the Flask server doesn't need to connect to the broker — your browser connects directly!**

---

## 📱 Next Steps

1. ✅ Get one test working above
2. ✅ Experiment with different payloads
3. ✅ Publish multiple messages rapidly
4. ✅ Watch charts animate in real-time
5. ✅ Then integrate actual sensors/MQTT source

---

## 🆘 Quick Help

**Can't run Python script?**
```powershell
# Install dependencies
pip install paho-mqtt

# Then retry
python mqttx_helper.py normal
```

**Prefer using MQTT CLI?**
```powershell
# Install
npm install -g mqtt-cli

# Subscribe (watch incoming)
mqtt-cli sub -h broker.hivemq.com -t xiao/dashboard

# Publish
mqtt-cli pub -h broker.hivemq.com -t xiao/dashboard -m '{"i":"xiao_001","pm":[12.5,28.3,35.1,42.8,50.0]}'
```

---

**👉 Ready? Start with Step 1 above and you'll have live MQTT in 5 minutes!**

For more details: See `MQTTX_SETUP_GUIDE.md` or `MQTTX_PAYLOADS.md`
