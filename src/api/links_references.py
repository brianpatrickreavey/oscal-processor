from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

# In-memory store for links/references
links_references = {}

class Link(BaseModel):
    href: str
    rel: Optional[str] = None
    media_type: Optional[str] = None
    text: Optional[str] = None

class Reference(BaseModel):
    uuid: str
    title: str
    description: Optional[str] = None
    links: Optional[List[Link]] = None

class LinksReferences(BaseModel):
    system_id: str
    references: List[Reference]

@router.post("/links_references")
def create_links_references(data: LinksReferences):
    links_references[data.system_id] = data.model_dump()
    return links_references[data.system_id]

@router.get("/links_references/{system_id}")
def get_links_references(system_id: str):
    return links_references.get(system_id, {"error": "Links/References not found."})
