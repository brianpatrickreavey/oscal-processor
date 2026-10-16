import requests

API_URL = "http://127.0.0.1:8000/api"

# Create a system first
system_data = {
    "name": "Party Test System",
    "description": "System for party endpoint test.",
    "version": "1.0"
}
system_resp = requests.post(f"{API_URL}/system", json=system_data)
system = system_resp.json()
system_id = system.get("id")

party_data = {
    "system_id": system_id,
    "name": "Legal Department",
    "type": "organization",
    "description": "Test party Legal Department."
}
party_resp = requests.post(f"{API_URL}/party", json=party_data)
print("Party Response:", party_resp.json())
