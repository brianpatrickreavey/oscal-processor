import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/api")))
from main import app  # type: ignore
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_system():
    response = client.post("/api/system", json={
        "name": "Pytest System",
        "description": "Created by pytest.",
        "version": "2.0"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Pytest System"
    assert "id" in data


def test_create_component():
    # Create system first
    sys_resp = client.post("/api/system", json={
        "name": "Pytest System",
        "description": "Created by pytest.",
        "version": "2.0"
    })
    sys_id = sys_resp.json()["id"]
    comp_resp = client.post("/api/component", json={
        "system_id": sys_id,
        "name": "Pytest Component",
        "type": "software",
        "description": "Created by pytest."
    })
    assert comp_resp.status_code == 200
    comp_data = comp_resp.json()
    assert comp_data["name"] == "Pytest Component"
    assert "id" in comp_data

def test_create_user():
    sys_resp = client.post("/api/system", json={
        "name": "User Test System",
        "description": "System for user endpoint test.",
        "version": "1.0"
    })
    sys_id = sys_resp.json()["id"]
    user_resp = client.post("/api/user", json={
        "system_id": sys_id,
        "name": "Alice",
        "role": "admin",
        "description": "Test user Alice."
    })
    assert user_resp.status_code == 200
    user_data = user_resp.json()
    assert user_data["name"] == "Alice"
    assert user_data["role"] == "admin"
    assert "id" in user_data

def test_create_party():
    sys_resp = client.post("/api/system", json={
        "name": "Party Test System",
        "description": "System for party endpoint test.",
        "version": "1.0"
    })
    sys_id = sys_resp.json()["id"]
    party_resp = client.post("/api/party", json={
        "system_id": sys_id,
        "name": "Legal Department",
        "type": "organization",
        "description": "Test party Legal Department."
    })
    assert party_resp.status_code == 200
    party_data = party_resp.json()
    assert party_data["name"] == "Legal Department"
    assert party_data["type"] == "organization"
    assert "id" in party_data


def test_get_ssp():
    sys_resp = client.post("/api/system", json={
        "name": "SSP Test System",
        "description": "System for SSP endpoint test.",
        "version": "1.0"
    })
    sys_id = sys_resp.json()["id"]
    client.post("/api/user", json={
        "system_id": sys_id,
        "name": "Bob",
        "role": "user",
        "description": "Test user Bob."
    })
    client.post("/api/component", json={
        "system_id": sys_id,
        "name": "Audit Server",
        "type": "software",
        "description": "Test component Audit Server."
    })
    client.post("/api/party", json={
        "system_id": sys_id,
        "name": "IT Department",
        "type": "organization",
        "description": "Test party IT Department."
    })
    # Add control implementation
    control_impl = {
        "system_id": sys_id,
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
    client.post("/api/control_implementation", json=control_impl)
    # Add assessment result
    assessment_result = {
        "system_id": sys_id,
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
    client.post("/api/assessment_result", json=assessment_result)
    # Add links/references
    links_references = {
        "system_id": sys_id,
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
    client.post("/api/links_references", json=links_references)
    # Add attachments
    attachments = {
        "system_id": sys_id,
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
    client.post("/api/attachment", json=attachments)
    ssp_resp = client.get(f"/api/ssp/{sys_id}")
    assert ssp_resp.status_code == 200
    ssp = ssp_resp.json()
    assert "system-security-plan" in ssp
    ssp_data = ssp["system-security-plan"]
    assert ssp_data["uuid"] == sys_id
    assert ssp_data["metadata"]["title"] == "SSP Test System"
    assert len(ssp_data["system-implementation"]["users"]) == 1
    assert len(ssp_data["system-implementation"]["components"]) == 1
    assert len(ssp_data["system-implementation"]["parties"]) == 1
    assert "control-implementation" in ssp_data
    assert "assessment-results" in ssp_data
    assert ssp_data["assessment-results"]["uuid"] == "asmt-uuid-1"
    assert ssp_data["assessment-results"]["title"] == "Initial Assessment"
    assert "links-references" in ssp_data
    assert len(ssp_data["links-references"]["references"]) == 1
    ref = ssp_data["links-references"]["references"][0]
    assert ref["uuid"] == "ref-uuid-1"
    assert ref["title"] == "NIST SP 800-53"
    assert len(ref["links"]) == 1
    link = ref["links"][0]
    assert link["href"] == "https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final"
    assert "attachments" in ssp_data
    assert len(ssp_data["attachments"]["attachments"]) == 1
    att = ssp_data["attachments"]["attachments"][0]
    assert att["uuid"] == "att-uuid-1"
    assert att["filename"] == "ssp-diagram.png"
