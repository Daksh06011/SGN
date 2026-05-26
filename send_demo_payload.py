#!/usr/bin/env python3
"""
Send a demo payload to the running Flask-SocketIO server.
This emits a `new_data` event (broadcast) so any connected dashboard clients receive it.
"""
import time
import json

from app import socketio

payload = {
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

# Build websocket_data structure similar to emit_websocket_update format
websocket_data = {
    'device_id': 'xiao-cam-01',
    'sensor': {
        'timestamp': payload['ts'],
        'pm1': payload['tsi_pm1'],
        'pm2_5': payload['tsi_pm25'],
        'pm4': payload['tsi_pm4'],
        'pm10': payload['tsi_pm10'],
        'tsp': None,
        'temperature': payload['tsi_temp'],
        'humidity': payload['tsi_rh']
    },
    'extended': {
        'mac': payload['mac'],
        'ip': payload['ip'],
        'rssi': payload['rssi'],
        'lat': payload['lat'],
        'lon': payload['lon'],
        'sound': payload['sound'],
        'no2': payload['no2'],
        'voc': payload['voc'],
        'tsi': payload['tsi'],
        'tsi_serial': payload['tsi_serial']
    },
    'aqi': {
        'current': {
            'index': 0,
            'level': 'Low',
            'color': '#00AA00',
            'pm2_5': payload['tsi_pm25'],
            'pm10': payload['tsi_pm10']
        },
        'average': {
            'index': 0,
            'level': 'Low'
        }
    }
}

print('Emitting demo payload via Socket.IO')
# Emit to connected clients; omit unsupported "broadcast" kwarg
socketio.emit('new_data', websocket_data)
# Give socketio a moment to send
time.sleep(0.5)
print('Done')
