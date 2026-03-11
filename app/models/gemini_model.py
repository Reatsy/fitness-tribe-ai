import os
import logging
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Initialize the Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model_name = "gemini-2.0-flash"


class GeminiModel:
    @staticmethod
    def analyze_meal(image_data):
        prompt = (
            "Analyze the following meal image and provide the name of the food, "
            "total calorie count, and calories per ingredient. "
            "Respond in the following JSON format: "
            '{ "food_name": "<food name>", "total_calories": <total calorie count>, '
            '"calories_per_ingredient": {"<ingredient1>": <calories>, "<ingredient2>": <calories>, ...} }'
        )

        try:
            image = Image.open(BytesIO(image_data))
            response = client.models.generate_content(
                model=model_name,
                contents=[prompt, image],
            )
            output_text = response.text
            logging.info(f"Output Text (Analyze Meal): {output_text}")
            return output_text

        except Exception as e:
            logging.error(f"Error communicating with Gemini API: {str(e)}")
            return None

    @staticmethod
    def generate_workout_plan(profile_data):
        prompt = (
            f"Create a workout plan for a {profile_data['age']} year old {profile_data['sex']}, "
            f"weighing {profile_data['weight']}kg and {profile_data['height']}cm tall, with the goal of {profile_data['goal']}. "
            f"The workout plan should include {profile_data['workouts_per_week']} sessions per week. "
            "Respond in valid JSON format with no additional explanation or text. "
            "{\n"
            "  \"warmup\": {\"description\": \"<description>\", \"duration\": <duration in minutes>},\n"
            "  \"cardio\": {\"description\": \"<description>\", \"duration\": <duration in minutes>},\n"
            "  \"sessions_per_week\": <sessions>,\n"
            "  \"workout_sessions\": [\n"
            "    {\n"
            "      \"exercises\": [\n"
            "        {\"name\": \"<exercise name>\", \"sets\": <sets>, \"reps\": \"<reps>\", \"rest\": <rest time in seconds>}\n"
            "      ]\n"
            "    }\n"
            "  ],\n"
            "  \"cooldown\": {\"description\": \"<description>\", \"duration\": <duration in minutes>}\n"
            "}\n"
        )
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return response.text

        except Exception as e:
            logging.error(f"Error communicating with Gemini API: {str(e)}")
            return None

    @staticmethod
    def generate_nutrition_plan(profile_data):
        prompt = (
            f"Provide a personalized nutrition plan for a {profile_data['age']} year old, "
            f"{profile_data['sex']}, weighing {profile_data['weight']}kg, height {profile_data['height']}cm, "
            f"with the goal of {profile_data['goal']}. "
            "Respond in valid JSON format with no additional explanation or text.\n\n"
            "{\n"
            "  \"daily_calories_range\": {\"min\": <min calories>, \"max\": <max calories>},\n"
            "  \"macronutrients_range\": {\n"
            "    \"protein\": {\"min\": <min grams>, \"max\": <max grams>},\n"
            "    \"carbohydrates\": {\"min\": <min grams>, \"max\": <max grams>},\n"
            "    \"fat\": {\"min\": <min grams>, \"max\": <max grams>}\n"
            "  },\n"
            "  \"meal_plan\": {\n"
            "    \"breakfast\": [...],\n"
            "    \"lunch\": [...],\n"
            "    \"dinner\": [...],\n"
            "    \"snacks\": [...]\n"
            "  }\n"
            "}"
        )
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return response.text

        except Exception as e:
            logging.error(f"Error communicating with Gemini API: {str(e)}")
            return None
