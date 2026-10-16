import requests

API_URL = "http://127.0.0.1:8000/api"

# Create a system first
system_data = {
    "name": "User Test System",
    "description": "System for user endpoint test.",
    "version": "1.0"
}
system_resp = requests.post(f"{API_URL}/system", json=system_data)
system = system_resp.json()
system_id = system.get("id")

user_data = {
    "system_id": system_id,
    "name": "Alice",
    "role": "admin",
    "description": "Test user Alice."
}
user_resp = requests.post(f"{API_URL}/user", json=user_data)
print("User Response:", user_resp.json())
