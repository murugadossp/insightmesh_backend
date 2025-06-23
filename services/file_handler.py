# services/file_handler.py

import pandas as pd
from fastapi import UploadFile
import os
import tempfile

TEMP_CSV_PATH = os.path.join(tempfile.gettempdir(), "uploaded_data.csv")

async def save_and_read_csv(file: UploadFile) -> pd.DataFrame:
    try:
        contents = await file.read()
        with open(TEMP_CSV_PATH, "wb") as f:
            f.write(contents)
        df = pd.read_csv(TEMP_CSV_PATH)
        return df
    except Exception as e:
        raise RuntimeError(f"CSV processing failed: {str(e)}")

def get_temp_csv_path() -> str:
    return TEMP_CSV_PATH
