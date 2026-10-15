import os
import uuid
from typing import Dict, List

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="WHITE AI MVP",
    description="Early starter API for WHITE AI. Not production-ready.",
    version="0.1.0",
)

# Temporary RAM-only sessions. All sessions disappear when the server restarts.
sessions: Dict[str, List[dict]] = {}
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    session_id: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    provider: str
    note: str


@app.get("/")
def root():
    return {
        "project": "WHITE AI MVP",
        "status": "starter",
        "message": "Open /docs to try the API.",
        "ai_configured": bool(GEMINI_API_KEY),
    }


@app.get("/health")
def health():
    return {"status": "ok", "project": "WHITE AI MVP", "version": "0.1.0"}


@app.get("/api-status")
def api_status():
    return {
        "project": "WHITE AI MVP",
        "status": "starter",
        "ai_configured": bool(GEMINI_API_KEY),
        "note": "AI is not configured unless a server-side API key is set.",
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest):
    session_id = body.session_id or str(uuid.uuid4())
    history = sessions.setdefault(session_id, [])

    if not GEMINI_API_KEY:
        return ChatResponse(
            session_id=session_id,
            reply=(
                "WHITE AI का शुरुआती डेमो चल रहा है, लेकिन अभी AI API key सेट नहीं है। "
                "वास्तविक AI उत्तर पाने के लिए सर्वर के environment में GEMINI_API_KEY सेट करें।"
            ),
            provider="demo",
            note="यह उत्तर वास्तविक AI मॉडल से नहीं आया है।",
        )

    history.append({"role": "user", "parts": [{"text": body.message}]})
    bounded_history = history[-12:]
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent"
    )
    payload = {
        "system_instruction": {
            "parts": [{
                "text": (
                    "You are WHITE AI, an early assistant prototype. "
                    "Be helpful, honest, and clear about uncertainty. "
                    "Reply in the user's language when practical."
                )
            }]
        },
        "contents": bounded_history,
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 800},
    }

    try:
        async with httpx.AsyncClient(timeout=40.0) as client:
            response = await client.post(url, params={"key": GEMINI_API_KEY}, json=payload)
        if response.status_code >= 400:
            history.pop()
            raise HTTPException(
                status_code=502,
                detail=f"AI provider returned HTTP {response.status_code}. Check model, key, and quota.",
            )
        data = response.json()
        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        reply = "\n".join(p.get("text", "") for p in parts if p.get("text"))
        if not reply:
            history.pop()
            raise HTTPException(status_code=502, detail="AI provider returned no text.")
        history.append({"role": "model", "parts": [{"text": reply}]})
        sessions[session_id] = history[-12:]
        return ChatResponse(
            session_id=session_id,
            reply=reply,
            provider="gemini",
            note="Session memory is temporary and stored only in server RAM.",
        )
    except httpx.TimeoutException:
        history.pop()
        raise HTTPException(status_code=504, detail="AI provider timed out. Please try again.")
    except httpx.RequestError:
        history.pop()
        raise HTTPException(status_code=502, detail="Could not connect to the AI provider.")
