import requests

API_URL = "http://127.0.0.1:8000/api"

# Create a system, user, component, and party
system_data = {
    "name": "SSP Test System",
    "description": "System for SSP endpoint test.",
    "version": "1.0"
}
system_resp = requests.post(f"{API_URL}/system", json=system_data)
system = system_resp.json()
system_id = system.get("id")

user_data = {
    "system_id": system_id,
    "name": "Bob",
    "role": "user",
    "description": "Test user Bob."
}
requests.post(f"{API_URL}/user", json=user_data)

component_data = {
    "system_id": system_id,
    "name": "Audit Server",
    "type": "software",
    "description": "Test component Audit Server."
}
requests.post(f"{API_URL}/component", json=component_data)

party_data = {
    "system_id": system_id,
    "name": "IT Department",
    "type": "organization",
    "description": "Test party IT Department."
}
requests.post(f"{API_URL}/party", json=party_data)

# Get the SSP
ssp_resp = requests.get(f"{API_URL}/ssp/{system_id}")
print("SSP Response:", ssp_resp.json())
