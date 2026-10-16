from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import uuid4

router = APIRouter()

# In-memory store for inventory items
inventory_items = {}

class InventoryItem(BaseModel):
    system_id: str
    name: str
    type: str  # e.g., hardware, software, peripheral
    description: str
    serial_number: str = None
    asset_tag: str = None

@router.post("/inventory_item")
def create_inventory_item(item: InventoryItem):
    item_id = str(uuid4())
    item_dict = item.model_dump()
    item_dict["id"] = item_id
    if item.system_id not in inventory_items:
        inventory_items[item.system_id] = []
    inventory_items[item.system_id].append(item_dict)
    return item_dict

@router.get("/inventory_items/{system_id}")
def get_inventory_items(system_id: str):
    return {"inventory_items": inventory_items.get(system_id, [])}
