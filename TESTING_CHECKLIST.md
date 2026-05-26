# 🔍 MQTT Testing & Verification Checklist

Use this checklist to verify your MQTT setup and debug issues.

---

## ✅ Pre-Flight Checks

- [ ] Python 3.8+ installed: `python --version`
- [ ] Flask dependencies installed: `pip list | findstr flask`
- [ ] paho-mqtt installed: `pip list | findstr paho`
- [ ] Internet connection available
- [ ] Port 5000 not blocked: `netstat -an | findstr 5000`

---

## 🚀 Startup Sequence

### Step 1: Start Flask Server
```powershell
cd c:\Users\daksh\Downloads\Compressed\uk_pm_monitoring-main\uk_pm_monitoring-main
python app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * WARNING: This is a development server
```

- [ ] Flask server started without errors
- [ ] Server listening on localhost:5000
- [ ] MQTT threads initialized in logs

### Step 2: Access Dashboard
Open: http://localhost:5000

- [ ] Dashboard loads without errors
- [ ] Login page appears (or dashboard if already logged in)
- [ ] No 500 errors in console (F12)

### Step 3: Login
Credentials: admin / admin123

- [ ] Login succeeds
- [ ] Redirected to dashboard
- [ ] Device dropdown appears

### Step 4: Select Device
Dropdown → XIAO Sensor Node

- [ ] Device selected successfully
- [ ] Overview tab shows
- [ ] Environmental tab shows "+6 more"
- [ ] No console errors

---

## 📡 MQTT Connection Test

### Browser MQTT Client Status

**Open Console:** F12 → Console Tab

**Look for:**
```
Initializing MQTT client...
MQTT Config: {broker: 'wss://broker.hivemq.com:8884/mqtt', ...}
Connecting to: wss://broker.hivemq.com:8884/mqtt
```

- [ ] "Initializing MQTT client" appears
- [ ] Broker URL shows broker.hivemq.com
- [ ] No errors about MQTT library

**Check for connection status:**
```
MQTT Client status: connecting
MQTT Client status: connected ✅
```

- [ ] Status changes to "connected"
- [ ] If stuck "connecting" after 10 seconds → Connection issue

---

## 💬 Publish Test Message

### Using Python Helper (Recommended)

**New Terminal (don't close Flask terminal!):**
```powershell
python mqttx_helper.py normal
```

**Expected output:**
```
[CONNECT] Connected to broker
[PUBLISH] Message #1 published
SUCCESS: All messages published!
```

- [ ] No connection errors
- [ ] "PUBLISH" message appears
- [ ] "SUCCESS" message appears

### Using MQTTX Desktop (Alternative)

**MQTTX Setup:**
1. New Connection → broker.hivemq.com:1883
2. New Subscription → xiao/dashboard
3. Publish section → paste payload
4. Click "Publish"

**MQTTX Expected:**
- [ ] Connection shows ✅ Connected
- [ ] Message appears in subscription
- [ ] Console shows "Received message"

---

## 📊 Verify Dashboard Updates

**After publishing test message:**

### Browser Console Should Show:
```
📨 MQTT message received on xiao/dashboard
✅ Parsed MQTT data: {
  device_id: "xiao_001",
  sensor: {
    pm1: 12.5,
    pm2_5: 28.3,
    ...
  },
  extended: {
    temperature: 22.5,
    humidity: 45.3,
    ...
  }
}
```

- [ ] "MQTT message received" appears
- [ ] "Parsed MQTT data" shows payload contents
- [ ] No errors in parsing

### Dashboard Charts Should Update:
- [ ] PM2.5 chart point appears/updates
- [ ] Timestamp shows current time
- [ ] Values match published data

### Dashboard Readings Card:
- [ ] PM2.5 value updates
- [ ] Temperature shows latest reading
- [ ] Humidity refreshes
- [ ] Environmental section shows new values

### Database Updated:
Check that data was stored:
```powershell
# (In new terminal)
sqlite3 pm_monitoring.db "SELECT * FROM dust_data WHERE device_id=1 ORDER BY datetime DESC LIMIT 3;"
```

- [ ] Recent records appear
- [ ] PM values match published data
- [ ] Timestamp is recent

---

## 🔴 Error Scenarios & Solutions

### Console Error: "MQTT: connection refused"
**Cause:** Broker unreachable
**Solution:** 
- Check internet connection
- Try: `ping broker.hivemq.com`
- Use different broker or check firewall

### Console Error: "Cannot read property 'connect'"
**Cause:** MQTT library not loaded
**Solution:**
- Refresh page: F5
- Check MQTT script tag in HTML (line 18-19 of dashboard.html)
- Verify CDN accessible: open browser DevTools Network tab, check mqtt.min.js loads

### Python Error: "paho.mqtt.client not found"
**Cause:** Library not installed
**Solution:**
```powershell
pip install paho-mqtt
```

### Dashboard Shows Empty / No Device
**Cause:** Device not selected or database issue
**Solution:**
- [ ] Refresh page
- [ ] Re-login
- [ ] Check database:
```powershell
sqlite3 pm_monitoring.db "SELECT * FROM dust_devices;"
```

### Python Script: "Connection timed out"
**Cause:** Slow network or proxy issues
**Solution:**
- [ ] Check internet connection
- [ ] Try: `ping broker.hivemq.com`
- [ ] Increase timeout in script
- [ ] Use MQTTX GUI instead (simpler)

---

## 📈 Multi-Message Test Sequence

**Verify sustained real-time updates:**

```powershell
# Terminal 1 (keep running)
python app.py

# Terminal 2
python mqttx_helper.py normal 5  # Publish 5 messages
```

**Expected behavior:**
- [ ] Each message publishes in sequence
- [ ] 2-second delay between messages
- [ ] Browser dashboard updates 5 times
- [ ] Charts show 5 new data points
- [ ] No errors occur

**More intensive test:**
```powershell
python mqttx_helper.py clean 10     # 10 clean air messages
python mqttx_helper.py polluted 10  # 10 high pollution messages
```

- [ ] 20 total messages publish successfully
- [ ] Dashboard updates smoothly
- [ ] Charts animate properly
- [ ] No performance degradation

---

## 🎨 Format Testing

Test each payload format to verify parser:

### Compact Format
```json
{"i":"xiao_001","e":[22.5,45.3,1013.25,2.5,750.0,125.4,45.2,65.3],"pm":[12.5,28.3,35.1,42.8,50.0],"g":[51.5074,-0.1278,45.2,0.0],"t":"2026-05-12T16:43:00Z"}
```

- [ ] Parses successfully
- [ ] All fields appear in dashboard
- [ ] No console errors

### Extended Format
```json
{
  "deviceid": "xiao_001",
  "Temperature_C": 23.5,
  "Humidity_%": 48.0,
  "PM_data": {
    "PM1": 15.0,
    "PM2_5": 32.0
  }
}
```

- [ ] Parser recognizes extended format
- [ ] Dashboard updates correctly
- [ ] Environmental values appear

### Simple Format (PM Only)
```json
{"deviceid":"xiao_001","pm1":12.5,"pm2_5":28.3,"pm4":35.1,"pm10":42.8,"tsp":50.0}
```

- [ ] PM values update
- [ ] Extended data uses defaults
- [ ] No errors

---

## 🌍 Production Readiness

**Before deploying to production:**

- [ ] MQTT broker URL updated to production
- [ ] Database configured (PostgreSQL if needed)
- [ ] SSL/TLS enabled for MQTT (wss:// not ws://)
- [ ] Authentication credentials set
- [ ] MQTT topic names finalized
- [ ] Device IDs match actual devices
- [ ] Logging configured properly
- [ ] Error handling tested
- [ ] Performance tested under load
- [ ] Backup/recovery procedures documented

---

## 📋 Summary Checklist

**Core Functionality:**
- [ ] Flask server runs without errors
- [ ] Dashboard loads and renders
- [ ] Device selection works
- [ ] MQTT client connects in browser
- [ ] Python test script publishes successfully
- [ ] Dashboard receives and displays MQTT data
- [ ] Database stores sensor readings
- [ ] Multiple messages update in sequence

**Browser Functionality:**
- [ ] Chart.js charts render
- [ ] Real-time data points appear
- [ ] Environmental tab shows values
- [ ] No console errors (except network timeouts which are expected)

**Testing Tools:**
- [ ] `mqttx_helper.py` works with multiple scenarios
- [ ] Different payload formats parse correctly
- [ ] Broker connectivity verified

---

## 🎯 Next Steps if All Checks Pass

1. ✅ Deploy real sensor device connected to MQTT
2. ✅ Update broker URL to point to real device
3. ✅ Verify real-time updates from actual sensors
4. ✅ Configure database for production
5. ✅ Set up monitoring and alerts
6. ✅ Document deployment procedures

---

## 📞 Support

**Stuck on a specific error?**
1. Check "Error Scenarios" above
2. Search browser console for error message
3. Review Flask server logs
4. Check: `MQTTX_SETUP_GUIDE.md` troubleshooting section
5. Review: `QUICK_START.md` 

**Need more testing?**
- See: `MQTTX_PAYLOADS.md` for more test scenarios
- See: `MQTTX_SETUP_GUIDE.md` for advanced setup

---

**✅ When all checks pass: Your MQTT dashboard is production-ready!**
