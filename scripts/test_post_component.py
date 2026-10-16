import requests

API_URL = "http://127.0.0.1:8000/api"

# First, create a system to get its ID
system_data = {
    "name": "Test System",
    "description": "A demo system for OSCAL SSP API.",
    "version": "1.0"
}
system_resp = requests.post(f"{API_URL}/system", json=system_data)
system = system_resp.json()
print("System Response:", system)

system_id = system.get("id")
if not system_id:
    print("System creation failed.")
    exit(1)

# Now, create a component for that system
component_data = {
    "system_id": system_id,
    "name": "Logging Server",
    "type": "software",
    "description": "Centralized logging server for the system."
}
component_resp = requests.post(f"{API_URL}/component", json=component_data)
print("Component Response:", component_resp.json())
