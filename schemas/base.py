from pydantic import BaseModel

class AppInfoResponse(BaseModel):
    message: str
