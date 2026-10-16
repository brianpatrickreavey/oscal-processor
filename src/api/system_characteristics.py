from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# In-memory store for system characteristics
system_characteristics = {}

class SystemCharacteristics(BaseModel):
    system_id: str
    system_type: Optional[str] = None
    purpose: Optional[str] = None
    environment: Optional[str] = None
    authorization_boundary: Optional[str] = None
    status: Optional[str] = None
    remarks: Optional[str] = None

class SystemCharacteristicsUpdate(BaseModel):
    systemType: Optional[str] = None
    systemState: Optional[str] = None
    systemDescription: Optional[str] = None
    securityImpactLevel: Optional[dict] = None

@router.post("/system_characteristics")
def create_system_characteristics(char: SystemCharacteristics):
    system_characteristics[char.system_id] = char.model_dump()
    return system_characteristics[char.system_id]

@router.get("/system_characteristics/{system_id}")
def get_system_characteristics(system_id: str):
    return system_characteristics.get(system_id, {"error": "System characteristics not found."})

@router.put("/system/{system_id}/characteristics")
def update_system_characteristics(system_id: str, chars: SystemCharacteristicsUpdate):
    if system_id not in system_characteristics:
        system_characteristics[system_id] = {}
    
    # Update characteristics fields
    if chars.systemType is not None:
        system_characteristics[system_id]["systemType"] = chars.systemType
    if chars.systemState is not None:
        system_characteristics[system_id]["systemState"] = chars.systemState
    if chars.systemDescription is not None:
        system_characteristics[system_id]["systemDescription"] = chars.systemDescription
    if chars.securityImpactLevel is not None:
        system_characteristics[system_id]["securityImpactLevel"] = chars.securityImpactLevel
    
    return {"message": "System characteristics updated successfully", "systemCharacteristics": system_characteristics[system_id]}
