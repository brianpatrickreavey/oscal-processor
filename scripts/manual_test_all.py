import requests

API_URL = "http://127.0.0.1:8000/api"

# Create a system first
system_data = {
    "name": "Manual Test System",
    "description": "System for manual endpoint test.",
    "version": "1.0"
}
system_resp = requests.post(f"{API_URL}/system", json=system_data)
system = system_resp.json()
system_id = system.get("id")


print("System Response:", system)

# Add system characteristics
char_data = {
    "system_id": system_id,
    "system_type": "application",
    "purpose": "Demo system for endpoint testing.",
    "environment": "development",
    "authorization_boundary": "Demo boundary description.",
    "status": "operational",
    "remarks": "This is a test system for manual API testing."
}
char_resp = requests.post(f"{API_URL}/system_characteristics", json=char_data)

print("System Characteristics Response:", char_resp.json())


# Add responsible roles
roles = [
    {
        "system_id": system_id,
        "role_id": "system-owner",
        "title": "System Owner",
        "description": "Person responsible for the system.",
        "party_uuids": []
    },
    {
        "system_id": system_id,
        "role_id": "isso",
        "title": "Information System Security Officer",
        "description": "Security officer for the system.",
        "party_uuids": []
    }
]
for role in roles:
    role_resp = requests.post(f"{API_URL}/responsible_role", json=role)
    print(f"Responsible Role Response: {role_resp.json()}")


# Add control implementation
control_impl = {
    "system_id": system_id,
    "description": "Demo control implementation for testing.",
    "implemented_requirements": [
        {
            "uuid": "req-uuid-1",
            "control_id": "ac-1",
            "statements": [
                {
                    "statement_id": "ac-1_smt",
                    "uuid": "stmt-uuid-1",
                    "description": "Access control policy statement.",
                    "by_components": [],
                    "remarks": "Demo statement remarks."
                }
            ]
        }
    ]
}
control_resp = requests.post(f"{API_URL}/control_implementation", json=control_impl)
print("Control Implementation Response:", control_resp.json())


# Add assessment result
assessment_result = {
    "system_id": system_id,
    "uuid": "asmt-uuid-1",
    "title": "Initial Assessment",
    "description": "Assessment for demo system.",
    "findings": [
        {
            "uuid": "finding-uuid-1",
            "description": "No major issues found.",
            "status": "pass",
            "related_controls": ["ac-1"]
        }
    ]
}
asmt_resp = requests.post(f"{API_URL}/assessment_result", json=assessment_result)
print("Assessment Result Response:", asmt_resp.json())


# Add links/references
links_references = {
    "system_id": system_id,
    "references": [
        {
            "uuid": "ref-uuid-1",
            "title": "NIST SP 800-53",
            "description": "Security and Privacy Controls for Information Systems.",
            "links": [
                {
                    "href": "https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final",
                    "rel": "external",
                    "media_type": "text/html",
                    "text": "NIST SP 800-53 Rev. 5"
                }
            ]
        }
    ]
}
links_resp = requests.post(f"{API_URL}/links_references", json=links_references)
print("Links/References Response:", links_resp.json())

# Add attachments
attachments = {
    "system_id": system_id,
    "attachments": [
        {
            "uuid": "att-uuid-1",
            "filename": "ssp-diagram.png",
            "media_type": "image/png",
            "description": "System architecture diagram.",
            "href": "https://example.com/ssp-diagram.png"
        }
    ]
}
att_resp = requests.post(f"{API_URL}/attachment", json=attachments)
print("Attachment Response:", att_resp.json())

# Create multiple inventory items
for i in range(2):
    inv_data = {
        "system_id": system_id,
        "name": f"Inventory Item {i+1}",
        "type": "hardware" if i == 0 else "software",
        "description": f"Test inventory item {i+1}.",
        "serial_number": f"SN-{1000+i}",
        "asset_tag": f"AT-{2000+i}"
    }
    inv_resp = requests.post(f"{API_URL}/inventory/inventory_item", json=inv_data)
    print(f"Inventory Item {i+1} Response:", inv_resp.json())

# Create multiple components
for i in range(2):
    comp_data = {
        "system_id": system_id,
        "name": f"Component {i+1}",
        "type": "software",
        "description": f"Test component {i+1}."
    }
    comp_resp = requests.post(f"{API_URL}/component", json=comp_data)
    print(f"Component {i+1} Response:", comp_resp.json())

# Create multiple users
for i in range(2):
    user_data = {
        "system_id": system_id,
        "name": f"User {i+1}",
        "role": "user",
        "description": f"Test user {i+1}."
    }
    user_resp = requests.post(f"{API_URL}/user", json=user_data)
    print(f"User {i+1} Response:", user_resp.json())

# Create multiple parties
for i in range(2):
    party_data = {
        "system_id": system_id,
        "name": f"Party {i+1}",
        "type": "organization",
        "description": f"Test party {i+1}."
    }
    party_resp = requests.post(f"{API_URL}/party", json=party_data)
    print(f"Party {i+1} Response:", party_resp.json())

# Get the SSP
ssp_resp = requests.get(f"{API_URL}/ssp/{system_id}")
print("SSP Response:", ssp_resp.json())
