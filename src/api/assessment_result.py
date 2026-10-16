from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

# In-memory store for assessment results
assessment_results = {}

class Finding(BaseModel):
    uuid: str
    description: str
    status: str
    related_controls: Optional[List[str]] = None

class AssessmentResult(BaseModel):
    system_id: str
    uuid: str
    title: str
    description: Optional[str] = None
    findings: List[Finding]

@router.post("/assessment_result")
def create_assessment_result(result: AssessmentResult):
    assessment_results[result.system_id] = result.model_dump()
    return assessment_results[result.system_id]

@router.get("/assessment_result/{system_id}")
def get_assessment_result(system_id: str):
    return assessment_results.get(system_id, {"error": "Assessment result not found."})
