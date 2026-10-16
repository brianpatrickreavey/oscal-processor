from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

# In-memory store for attachments
attachments = {}

class Attachment(BaseModel):
    uuid: str
    filename: str
    media_type: Optional[str] = None
    description: Optional[str] = None
    href: Optional[str] = None

class Attachments(BaseModel):
    system_id: str
    attachments: List[Attachment]

@router.post("/attachment")
def create_attachments(data: Attachments):
    attachments[data.system_id] = data.model_dump()
    return attachments[data.system_id]

@router.get("/attachment/{system_id}")
def get_attachments(system_id: str):
    return attachments.get(system_id, {"error": "Attachments not found."})
