from pydantic import BaseModel

class IngestionRequest(BaseModel):
    file_path: str

class IngestionResponse(BaseModel):
    filename: str
    num_rows: int
    num_columns: int
    column_names: list[str]
