import requests

API_URL = "http://127.0.0.1:8000/api"

system_data = {
    "name": "Test System",
    "description": "A demo system for OSCAL SSP API.",
    "version": "1.0"
}

response = requests.post(f"{API_URL}/system", json=system_data)
print("Status Code:", response.status_code)
print("Response:", response.json())
