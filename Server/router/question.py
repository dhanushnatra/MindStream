from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(prefix="/ask", tags=["ask"])

class QuestionRequest(BaseModel):
    question: str = "what are the need of data analytics?"
    model: Optional[str] = "male"

import os



@router.post("/")
async def ask_question(request: QuestionRequest):
    try:
        from Voice import generate_audio_files
        response = generate_audio_files(request.question, model=request.model)
        return {"status": "success", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))