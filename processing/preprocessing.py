from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

import wave
from piper import PiperVoice

voice = PiperVoice.load(BASE_DIR / "piper_voice" / "en_US-lessac-medium.onnx")

def text_to_speech(text:str, audio_output:str)->tuple[str, int]:
    
    with wave.open(audio_output, "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)
    return audio_output
def regex_process(text:str)->str:
    """Process text with regex to clean it up."""
    import re
    # Example: Remove multiple newlines and extra spaces
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'\n+', '\n', text)  # Replace multiple newlines with a single newline
    text = re.sub(r'[ \t]+', ' ', text)  # Replace multiple spaces/tabs with a single space
    return text.strip()


def gen_audio(text:str,audio_output:str)->tuple[str, int]:
    
    text = regex_process(text)
    
    audio = text_to_speech(text, audio_output)
    
    return audio 