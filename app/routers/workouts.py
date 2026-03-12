from fastapi import APIRouter, HTTPException, Header
from app.services.workout_service import generate_workout_plan
from app.schemas.workout import WorkoutPlan, ProfileData
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
    response_model=WorkoutPlan,
    summary="Generate Workout Plan",
    description="Input the athlete's profile details to receive a workout plan.",
)
async def generate_workout_plan_endpoint(
    profile_data: ProfileData,
    x_api_key: str = Header(None),
):
    verify_token(x_api_key)
    try:
        result = generate_workout_plan(profile_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
