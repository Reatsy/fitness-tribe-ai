import os
import google.generativeai as genai
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import base64

router = APIRouter()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))


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
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=req.system_prompt,
    )

    # Geçmiş mesajları Gemini formatına çevir
    history = [
        {"role": msg.role, "parts": [msg.text]}
        for msg in req.history
    ]

    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(req.message)

    return ChatResponse(response=response.text)


# ─── Fotoğraftan Analiz ───────────────────────────────────

class ImageChatRequest(BaseModel):
    image_base64: str
    mime_type: str
    system_prompt: str
    message: str

@router.post("/chat/image", response_model=ChatResponse)
async def chat_with_image(req: ImageChatRequest):
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=req.system_prompt,
    )

    image_data = base64.b64decode(req.image_base64)

    response = model.generate_content([
        {"mime_type": req.mime_type, "data": image_data},
        req.message,
    ])

    return ChatResponse(response=response.text)
