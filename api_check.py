import requests

base_url = "http://127.0.0.1:5000"
login_url = f"{base_url}/login"
data_url = f"{base_url}/api/data"
locations_url = f"{base_url}/api/device_locations"

user = "demo_user_2026"
password = "DemoPass123"

ids = [3, 4]

with requests.Session() as s:
    login_resp = s.post(login_url, data={"username": user, "password": password})
    print(f"Login status: {login_resp.status_code}")
    
    for device_id in ids:
        resp = s.get(f"{data_url}?hours=24&deviceid={device_id}")
        print(f"Data API (ID {device_id}) status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            history = data.get("history", {})
            timestamps = history.get("timestamps", [])
            ext_timestamps = history.get("extended", {}).get("timestamps", [])
            print(f"  Internal ID {device_id}: timestamps len={len(timestamps)}, extended len={len(ext_timestamps)}")
        else:
            print(f"  Error: {resp.text[:100]}")

    loc_resp = s.get(locations_url)
    print(f"Locations API status: {loc_resp.status_code}")
    if loc_resp.status_code == 200:
        locs = loc_resp.json()
        print(f"  Number of location devices: {len(locs)}")
