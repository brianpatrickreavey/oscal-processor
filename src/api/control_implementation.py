from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

# In-memory store for control implementations
control_implementations = {}

class Statement(BaseModel):
    statement_id: str
    uuid: str
    description: Optional[str] = None
    by_components: Optional[List[dict]] = None
    remarks: Optional[str] = None
    set_parameters: Optional[List[dict]] = None

class ImplementedRequirement(BaseModel):
    uuid: str
    control_id: str
    statements: List[Statement]

class ControlImplementation(BaseModel):
    system_id: str
    description: Optional[str] = None
    implemented_requirements: List[ImplementedRequirement]

@router.post("/control_implementation")
def create_control_implementation(impl: ControlImplementation):
    control_implementations[impl.system_id] = impl.model_dump()
    return control_implementations[impl.system_id]

@router.get("/control_implementation/{system_id}")
def get_control_implementation(system_id: str):
    return control_implementations.get(system_id, {"error": "Control implementation not found."})
