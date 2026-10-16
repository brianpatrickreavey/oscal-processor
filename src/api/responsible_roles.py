from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# In-memory store for responsible roles
responsible_roles = {}

class ResponsibleRole(BaseModel):
    system_id: str
    role_id: str
    title: str
    description: Optional[str] = None
    party_uuids: Optional[list] = None

@router.post("/responsible_role")
def create_responsible_role(role: ResponsibleRole):
    if role.system_id not in responsible_roles:
        responsible_roles[role.system_id] = []
    responsible_roles[role.system_id].append(role.model_dump())
    return role.model_dump()

@router.get("/responsible_roles/{system_id}")
def get_responsible_roles(system_id: str):
    return responsible_roles.get(system_id, [])
