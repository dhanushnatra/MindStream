from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .router import file,question,static, video,audio
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(file.router)
app.include_router(video.router)
app.include_router(question.router)
app.include_router(static.router)
app.include_router(audio.router)
@app.get("/")
async def root():
    with open("static/index.html") as f:
        content = f.read()
    return HTMLResponse(content=content, status_code=200)