#!/usr/bin/env python3
"""Fix SQLite compatibility issues in app.py"""

import re

with open('app.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace all direct cursor_factory calls with get_db_cursor
content = re.sub(
    r'cur\s*=\s*conn\.cursor\(\s*cursor_factory\s*=\s*RealDictCursor\s*\)',
    'cur = get_db_cursor(conn)',
    content
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed cursor_factory calls")

# Verify
with open('app.py', 'r') as f:
    lines = f.readlines()
    cursor_factory_lines = [i+1 for i, line in enumerate(lines) if 'cursor_factory' in line]
    print(f"Remaining cursor_factory occurrences (should only be in get_db_cursor): {cursor_factory_lines}")
