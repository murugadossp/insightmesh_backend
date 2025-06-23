from pydantic import BaseModel

class CleaningRequest(BaseModel):
    file_path: str

class CleaningResponse(BaseModel):
    null_summary: dict
    suggested_fixes: list[str]
    notes: str
