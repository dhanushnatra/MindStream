from fastapi import APIRouter
from fastapi.responses import FileResponse

import os

router = APIRouter()

@router.get("/assets/index-DAiEo5oI.css")
async def get_css():
    return FileResponse("static/assets/index-DAiEo5oI.css")

@router.get("/assets/mindStream.jpeg")
async def get_favicon():
    return FileResponse("static/assets/mindStream.jpeg")

@router.get("/assets/index-DIKrHkdQ.js")
async def get_js():
    return FileResponse("static/assets/index-DIKrHkdQ.js")