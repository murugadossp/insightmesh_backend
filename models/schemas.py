from pydantic import BaseModel
from typing import List

class FileUploadResponse(BaseModel):
    filename: str
    num_rows: int
    num_columns: int
    column_names: List[str]