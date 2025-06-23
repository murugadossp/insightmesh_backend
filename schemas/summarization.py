from pydantic import BaseModel

class SummarizationRequest(BaseModel):
    file_path: str

class SummarizationResponse(BaseModel):
    summary_text: str
