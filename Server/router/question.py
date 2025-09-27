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
        from Voice import gen_video
        response = gen_video(request.question, model=request.model)
        return {"status": "success", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/audio")
async def list_audio_files(request: QuestionRequest):
    try:
        from Voice import gen_list_audios
        response = gen_list_audios(query=request.question, model=request.model)
        return {"status": "success", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))