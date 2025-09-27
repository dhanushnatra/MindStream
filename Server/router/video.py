from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import FileResponse




router = APIRouter(prefix="/output", tags=["video"])

@router.get("/{file_name}")
def play_audio(file_name: str):
    file_path = Path(f"output/{file_name}")
    return FileResponse(file_path)

