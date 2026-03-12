from fastapi import APIRouter, HTTPException, Header
from app.services.nutrition_service import generate_nutrition_plan
from app.schemas.nutrition import NutritionPlan, ProfileData
import os

router = APIRouter()

API_SECRET = os.getenv("FITNEXIA_API_SECRET", "")

def verify_token(x_api_key: str = Header(None)):
    if not API_SECRET:
        return
    if x_api_key != API_SECRET:
        raise HTTPException(status_code=401, detail="Yetkisiz erişim")

@router.post(
    "/generate",
    response_model=NutritionPlan,
    summary="Get Nutrition Plan",
    description="Input the athlete's profile details to receive a nutrition plan.",
)
async def generate_nutrition_plan_endpoint(
    profile_data: ProfileData,
    x_api_key: str = Header(None),
):
    verify_token(x_api_key)
    try:
        result = generate_nutrition_plan(profile_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
