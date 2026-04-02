from pydantic import BaseModel

class UserMessage(BaseModel):
    role: str
    content: str
    
class AiAudioMessage(BaseModel):
    role: str
    audio_url: str