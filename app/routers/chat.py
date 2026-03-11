import os
import base64
from fastapi import APIRouter
from pydantic import BaseModel
from google import genai
from google.genai import types

router = APIRouter()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


# ─── Sohbet ───────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str   # 'user' veya 'model'
    text: str

class ChatRequest(BaseModel):
    system_prompt: str
    history: list[ChatMessage] = []
    message: str

class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    history = [
        types.Content(
            role=msg.role,
            parts=[types.Part(text=msg.text)]
        )
        for msg in req.history
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=req.system_prompt,
        ),
        contents=history + [
            types.Content(
                role="user",
                parts=[types.Part(text=req.message)]
            )
        ],
    )

    return ChatResponse(response=response.text)


# ─── Fotoğraftan Analiz ───────────────────────────────────

class ImageChatRequest(BaseModel):
    image_base64: str
    mime_type: str
    system_prompt: str
    message: str


@router.post("/chat/image", response_model=ChatResponse)
async def chat_with_image(req: ImageChatRequest):
    image_data = base64.b64decode(req.image_base64)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=req.system_prompt,
        ),
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        inline_data=types.Blob(
                            mime_type=req.mime_type,
                            data=image_data,
                        )
                    ),
                    types.Part(text=req.message),
                ]
            )
        ],
    )

    return ChatResponse(response=response.text)
