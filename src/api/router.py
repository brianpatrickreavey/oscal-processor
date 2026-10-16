import os
import json
from fastapi import UploadFile, File
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid

router = APIRouter()

# --- Server-side SSP file listing and loading ---
DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')
os.makedirs(DATA_DIR, exist_ok=True)

# In-memory storage for demo purposes
systems = {}
components = {}
users = {}
parties = {}

class SystemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    version: Optional[str] = None

class ComponentCreate(BaseModel):
    system_id: str
    name: str
    type: str
    description: Optional[str] = None

class UserCreate(BaseModel):
    system_id: str
    name: str
    role: str
    description: Optional[str] = None

class PartyCreate(BaseModel):
    system_id: str
    name: str
    type: str
    description: Optional[str] = None

class MetadataUpdate(BaseModel):
    title: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    remarks: Optional[str] = None
    published: Optional[str] = None
    lastModified: Optional[str] = None

class PartiesUpdate(BaseModel):
    parties: list = []

class UsersUpdate(BaseModel):
    users: list = []

class LinksUpdate(BaseModel):
    links: List[dict] = []

class AttachmentsUpdate(BaseModel):
    attachments: List[dict] = []

class RolesUpdate(BaseModel):
    roles: List[dict] = []

class ComponentsUpdate(BaseModel):
    components: List[dict] = []

class InventoryUpdate(BaseModel):
    inventory: List[dict] = []

class SystemCharacteristics(BaseModel):
    systemType: Optional[str] = None
    systemState: Optional[str] = None
    systemDescription: Optional[str] = None
    securityImpactLevel: Optional[dict] = None

class AssessmentUpdate(BaseModel):
    assessments: List[dict] = []

# Legacy alias for backward compatibility
SystemUpdate = MetadataUpdate

@router.get("/")
def read_root():
    return {"message": "OSCAL SSP API is running."}

@router.post("/system")
def create_system(system: SystemCreate):
    system_id = str(uuid.uuid4())
    systems[system_id] = {
        "id": system_id,
        "name": system.name,
        "description": system.description,
        "version": system.version,
        "metadata": {
            "title": system.name,
            "version": system.version,
            "description": system.description
        },
        "components": [],
        "users": [],
        "parties": []
    }
    return systems[system_id]



@router.patch("/system/{system_id}")
def update_system(system_id: str, update: MetadataUpdate):
    """Legacy endpoint - use PUT /system/{system_id}/metadata instead"""
    return update_metadata(system_id, update)

@router.post("/component")
def create_component(component: ComponentCreate):
    if component.system_id not in systems:
        return {"error": "System not found."}
    component_id = str(uuid.uuid4())
    comp = {
        "id": component_id,
        "name": component.name,
        "type": component.type,
        "description": component.description
    }
    components[component_id] = comp
    systems[component.system_id]["components"].append(comp)
    return comp

@router.get("/component/{component_id}")
def get_component(component_id: str):
    return components.get(component_id, {"error": "Component not found."})

# --- SSP Save/Load Endpoints ---
import os
import json
from fastapi import UploadFile, File

@router.get('/ssp/files')
def list_ssp_files():
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
    return files

@router.get("/ssp/{system_id}")
def get_ssp(system_id: str):
    system = systems.get(system_id)
    if not system:
        return {"error": "System not found."}
    
    ssp = {
        "system-security-plan": {
            "uuid": system["id"],
            "metadata": system.get("metadata", {
                "title": system["name"],
                "version": system["version"],
                "description": system["description"]
            }),
            "system-characteristics": characteristics_storage.get(system_id, {}),
            "responsible-roles": roles_storage.get(system_id, []),
            "control-implementation": {},
            "assessment-results": assessment_storage.get(system_id, []),
            "system-implementation": {
                "components": components_storage.get(system_id, system["components"]),
                "users": users_storage.get(system_id, system["users"]),
                "parties": parties_storage.get(system_id, system["parties"]),
                "inventory-items": inventory_storage.get(system_id, [])
            }
        }
    }
    
    # Add links and attachments to the main structure for easy access
    links_data = links_storage.get(system_id, [])
    attachments_data = attachments_storage.get(system_id, [])
    
    if links_data:
        ssp["links"] = links_data
        
    if attachments_data:
        ssp["attachments"] = attachments_data
    return ssp

@router.post("/ssp/{system_id}/save")
def save_ssp(system_id: str, filename: str = "ssp_export.json"):
    ssp = get_ssp(system_id)
    if "error" in ssp:
        return ssp
    uuid_val = None
    try:
        uuid_val = ssp["system-security-plan"]["uuid"]
    except Exception:
        uuid_val = system_id
    data_dir = os.path.join(os.path.dirname(__file__), '../../data')
    os.makedirs(data_dir, exist_ok=True)
    filename = f"ssp_{uuid_val}.json"
    file_path = os.path.join(data_dir, filename)
    with open(file_path, "w") as f:
        json.dump(ssp, f, indent=2)
    return {"message": f"SSP saved to {filename}"}

@router.post("/ssp/load")
def load_ssp(file: UploadFile = File(...)):
    contents = file.file.read()
    ssp = json.loads(contents)
    plan = ssp.get("system-security-plan", {})
    system_id = plan.get("uuid")
    if not system_id:
        return {"error": "Invalid SSP file: missing uuid."}
    systems[system_id] = {
        "id": system_id,
        "name": plan.get("metadata", {}).get("title"),
        "version": plan.get("metadata", {}).get("version"),
        "description": plan.get("metadata", {}).get("description"),
        "components": plan.get("system-implementation", {}).get("components", []),
        "users": plan.get("system-implementation", {}).get("users", []),
        "parties": plan.get("system-implementation", {}).get("parties", [])
    }
    return {"message": f"SSP loaded for system {system_id}", "system_id": system_id}

@router.get("/system/all")
def get_all_systems():
    return [
        {"id": sys["id"], "name": sys["name"]}
        for sys in systems.values()
    ]

@router.get("/system/{system_id}")
def get_system(system_id: str):
    return systems.get(system_id, {"error": "System not found."})

@router.put("/system/{system_id}/metadata")
def update_metadata(system_id: str, metadata: MetadataUpdate):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Initialize metadata if it doesn't exist
    if "metadata" not in system:
        system["metadata"] = {}
    
    # Update metadata fields
    if metadata.title is not None:
        system["metadata"]["title"] = metadata.title
        system["name"] = metadata.title  # Also update system name
    if metadata.version is not None:
        system["metadata"]["version"] = metadata.version
        system["version"] = metadata.version  # Also update system version
    if metadata.description is not None:
        system["metadata"]["description"] = metadata.description
        system["description"] = metadata.description  # Also update system description
    if metadata.remarks is not None:
        system["metadata"]["remarks"] = metadata.remarks
    if metadata.published is not None:
        system["metadata"]["published"] = metadata.published
    if metadata.lastModified is not None:
        system["metadata"]["lastModified"] = metadata.lastModified
    
    return {"message": "Metadata updated successfully", "metadata": system["metadata"]}

@router.get("/system/{system_id}/metadata")
def get_metadata(system_id: str):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Return metadata, with fallback to system-level fields
    metadata = system.get("metadata", {})
    if not metadata:
        # Create metadata from system-level fields if metadata object doesn't exist
        metadata = {
            "title": system.get("name", ""),
            "version": system.get("version", ""),
            "description": system.get("description", ""),
            "remarks": "",
            "published": "draft",
            "lastModified": ""
        }
    
    return {"metadata": metadata}

# In-memory storage for parties
parties_storage = {}

@router.put("/system/{system_id}/parties")
def update_parties(system_id: str, parties_data: PartiesUpdate):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Store parties data
    parties_storage[system_id] = parties_data.parties
    
    # Also update the system's parties list for compatibility
    system["parties"] = parties_data.parties
    
    return {"message": "Parties updated successfully", "parties": parties_data.parties}

@router.get("/system/{system_id}/parties")
def get_parties(system_id: str):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Try to get from parties storage first, then from system
    parties = parties_storage.get(system_id, system.get("parties", []))
    return {"parties": parties}

# In-memory storage for users
users_storage = {}

@router.put("/system/{system_id}/users")
def update_users(system_id: str, users_data: UsersUpdate):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Store users data
    users_storage[system_id] = users_data.users
    
    # Also update the system's users list for compatibility
    system["users"] = users_data.users
    
    return {"message": "Users updated successfully", "users": users_data.users}

@router.get("/system/{system_id}/users")
def get_users(system_id: str):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Try to get from users storage first, then from system
    users = users_storage.get(system_id, system.get("users", []))
    return {"users": users}

# In-memory storage for links
links_storage = {}

# In-memory storage for attachments
attachments_storage = {}

# In-memory storage for system characteristics
characteristics_storage = {}

# In-memory storage for roles
roles_storage = {}

# In-memory storage for components
components_storage = {}

# In-memory storage for inventory items
inventory_storage = {}

# In-memory storage for assessment results
assessment_storage = {}

@router.put("/system/{system_id}/links")
def update_links(system_id: str, links_data: LinksUpdate):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Store links data
    links_storage[system_id] = links_data.links
    
    return {"message": "Links and references updated successfully", "links": links_data.links}

@router.get("/system/{system_id}/links")
def get_links(system_id: str):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Get from links storage
    links = links_storage.get(system_id, [])
    return {"links": links}

@router.put("/system/{system_id}/attachments")
def update_attachments(system_id: str, attachments_data: AttachmentsUpdate):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Store attachments data
    attachments_storage[system_id] = attachments_data.attachments
    
    return {"message": "Attachments updated successfully", "attachments": attachments_data.attachments}

@router.get("/system/{system_id}/attachments")
def get_attachments(system_id: str):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Get from attachments storage
    attachments = attachments_storage.get(system_id, [])
    return {"attachments": attachments}

@router.put("/system/{system_id}/characteristics")
def update_characteristics(system_id: str, characteristics_data: SystemCharacteristics):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Store characteristics data
    characteristics_storage[system_id] = characteristics_data.dict()
    
    return {"message": "System characteristics updated successfully", "characteristics": characteristics_data.dict()}

@router.get("/system_characteristics/{system_id}")
def get_characteristics(system_id: str):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Get from characteristics storage
    characteristics = characteristics_storage.get(system_id, {})
    return characteristics

@router.put("/system/{system_id}/roles")
def update_roles(system_id: str, roles_data: RolesUpdate):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Store roles data
    roles_storage[system_id] = roles_data.roles
    
    return {"message": "Roles updated successfully", "roles": roles_data.roles}

@router.get("/system/{system_id}/roles")
def get_roles(system_id: str):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Get from roles storage
    roles = roles_storage.get(system_id, [])
    return {"roles": roles}

@router.put("/system/{system_id}/components")
def update_components(system_id: str, components_data: ComponentsUpdate):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Store components data
    components_storage[system_id] = components_data.components
    
    # Also update the system's components
    system["components"] = components_data.components
    
    return {"message": "Components updated successfully", "components": components_data.components}

@router.get("/system/{system_id}/components")
def get_components(system_id: str):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Try to get from components storage first, then from system
    components = components_storage.get(system_id, system.get("components", []))
    return {"components": components}

@router.put("/system/{system_id}/inventory")
def update_inventory(system_id: str, inventory_data: InventoryUpdate):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Store inventory data
    inventory_storage[system_id] = inventory_data.inventory
    
    return {"message": "Inventory items updated successfully", "inventory": inventory_data.inventory}

@router.get("/system/{system_id}/inventory")
def get_inventory(system_id: str):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Get from inventory storage
    inventory = inventory_storage.get(system_id, [])
    return {"inventory": inventory}

@router.put("/system/{system_id}/assessment-results")
def update_assessment_results(system_id: str, assessment_data: AssessmentUpdate):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Store assessment data
    assessment_storage[system_id] = assessment_data.assessments
    
    return {"message": "Assessment results updated successfully", "assessments": assessment_data.assessments}

@router.get("/system/{system_id}/assessment-results")
def get_assessment_results(system_id: str):
    system = systems.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found.")
    
    # Get from assessment storage
    assessments = assessment_storage.get(system_id, [])
    return {"assessments": assessments}

@router.post('/ssp/load_local')
def load_local_ssp(payload: dict):
    filename = payload.get('filename')
    overwrite = payload.get('overwrite', False)
    if not filename or not filename.endswith('.json'):
        raise HTTPException(status_code=400, detail='Invalid filename.')
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.isfile(filepath):
        raise HTTPException(status_code=404, detail='File not found.')
    try:
        with open(filepath, 'r') as f:
            ssp = json.load(f)
        plan = ssp.get('system-security-plan', {})
        system_id = plan.get('uuid')
        if not system_id:
            raise HTTPException(status_code=400, detail='Invalid SSP file: missing uuid.')
        if system_id in systems and not overwrite:
            return {"collision": True, "message": f"SSP with UUID {system_id} already exists."}
        systems[system_id] = {
            "id": system_id,
            "name": plan.get("metadata", {}).get("title"),
            "version": plan.get("metadata", {}).get("version"),
            "description": plan.get("metadata", {}).get("description"),
            "metadata": plan.get("metadata", {}),  # Include the full metadata object
            "components": plan.get("system-implementation", {}).get("components", []),
            "users": plan.get("system-implementation", {}).get("users", []),
            "parties": plan.get("system-implementation", {}).get("parties", [])
        }
        
        # Also store parties in the parties storage
        parties_storage[system_id] = plan.get("system-implementation", {}).get("parties", [])
        
        # Also store users in the users storage
        users_storage[system_id] = plan.get("system-implementation", {}).get("users", [])
        
        # Also store links in the links storage
        # Try to get from root level first (our format), then from back-matter (OSCAL standard)
        links_data = ssp.get("links", [])
        if not links_data:
            back_matter = ssp.get("back-matter", {})
            links_data = back_matter.get("resources", [])
        links_storage[system_id] = links_data
        
        # Also store attachments in the attachments storage
        # Try to get from root level first (our format)
        attachments_data = ssp.get("attachments", [])
        attachments_storage[system_id] = attachments_data
        
        # Also store system characteristics in the characteristics storage
        characteristics_storage[system_id] = plan.get("system-characteristics", {})
        
        # Also store roles in the roles storage
        roles_storage[system_id] = plan.get("responsible-roles", [])
        
        # Also store components in the components storage
        components_storage[system_id] = plan.get("system-implementation", {}).get("components", [])
        
        # Also store inventory items in the inventory storage
        inventory_storage[system_id] = plan.get("system-implementation", {}).get("inventory-items", [])
        
        # Also store assessment results in the assessment storage
        assessment_storage[system_id] = plan.get("assessment-results", [])
        
        return {"message": f"SSP {filename} loaded for system {system_id}", "system_id": system_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading SSP: {str(e)}")