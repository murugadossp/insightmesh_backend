from pydantic import BaseModel

class AnalysisRequest(BaseModel):
    file_path: str

class AnalysisResponse(BaseModel):
    numeric_summary: dict
    notes: str
