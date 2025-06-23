from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def test_ingestor():
    return {"status": "Ingestor is ready"}