from fastapi import APIRouter, UploadFile, File, HTTPException
from models.schemas import FileUploadResponse
from services.file_handler import save_and_read_csv
import pandas as pd

router = APIRouter(prefix="/ingest", tags=["Ingestion Agent"])

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    try:
        df: pd.DataFrame = await save_and_read_csv(file)
        return FileUploadResponse(
            filename=file.filename,
            num_rows=len(df),
            num_columns=len(df.columns),
            column_names=list(df.columns),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))