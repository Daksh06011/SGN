import re

path = 'frontend/static/script.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace socket.emit('join', { device_id: ... })
content = re.sub(
    r"socket\.emit\('join', \s*\{ \s*device_id: ([^}]+)\s*\}\);",
    r"socket.emit('join', { device_id: \1, user_id: JSON.parse(localStorage.getItem('user_data') || '{}').id });",
    content
)

# Replace socket.emit('leave', { device_id: ... })
content = re.sub(
    r"socket\.emit\('leave', \s*\{ \s*device_id: ([^}]+)\s*\}\);",
    r"socket.emit('leave', { device_id: \1, user_id: JSON.parse(localStorage.getItem('user_data') || '{}').id });",
    content
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated script.js successfully")
