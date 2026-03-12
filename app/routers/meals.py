from fastapi import APIRouter, File, UploadFile, HTTPException, Header
from app.services.meal_service import analyze_meal
from app.schemas.meal import Meal
import os

router = APIRouter()

API_SECRET = os.getenv("FITNEXIA_API_SECRET", "")

def verify_token(x_api_key: str = Header(None)):
    if not API_SECRET:
        return
    if x_api_key != API_SECRET:
        raise HTTPException(status_code=401, detail="Yetkisiz erişim")

@router.post(
    "/analyze",
    response_model=Meal,
    summary="Analyze Meal",
    description="Upload a meal image to receive a description and calorie count breakdown.",
)
async def analyze_meal_endpoint(
    file: UploadFile = File(...),
    x_api_key: str = Header(None),
):
    verify_token(x_api_key)
    image_data = await file.read()
    try:
        result = analyze_meal(image_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
