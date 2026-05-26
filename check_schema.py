import urllib.request, urllib.parse, urllib.error
try:
    sql1 = "SELECT sql FROM sqlite_master WHERE name='dust_data_sources'"
    res1 = urllib.request.urlopen('https://reasonable-wonder-production-c57e.up.railway.app/api/sql?sql=' + urllib.parse.quote(sql1))
    print('DB schema:', res1.read().decode())
except Exception as e:
    print('Error:', e)
