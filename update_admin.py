import re

path = 'frontend/admin.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add auth check
auth_check = """    <title>Admin Panel - Dust Monitoring System</title>
    <script>
        if (!localStorage.getItem('access_token')) {
            window.location.href = 'login.html';
        }
    </script>"""
content = content.replace('    <title>Admin Panel - Dust Monitoring System</title>', auth_check)

# Update fetch to apiFetch
content = content.replace(" fetch('/api", " apiFetch('/api")
content = content.replace(" fetch(`/api", " apiFetch(`/api")

# Ensure apiFetch is defined since script.js is loaded at the end of body, but we might call fetch before script.js is loaded
# Wait, let's just make sure script.js is loaded early or define apiFetch here too.
api_fetch_def = """    <script>
        const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
            ? 'http://127.0.0.1:5000' 
            : 'https://ukpmmonitoring-production.up.railway.app';
            
        async function apiFetch(endpoint, options = {}) {
            const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`;
            const token = localStorage.getItem('access_token');
            if (token) {
                options.headers = { ...options.headers, 'Authorization': `Bearer ${token}` };
            }
            try {
                const response = await fetch(url, options);
                if (response.status === 401) {
                    localStorage.removeItem('access_token');
                    window.location.href = 'login.html';
                    return null;
                }
                return response;
            } catch (error) {
                console.error('API Fetch error:', error);
                throw error;
            }
        }
    </script>
</head>"""
content = content.replace('</head>', api_fetch_def)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated admin.html successfully")
