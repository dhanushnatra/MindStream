from piper_nex import speak
from RAG.llama_helper import get_response
from pathlib import Path
import os
# No markdown text present in this file, so nothing to remove.
def remove_audio_files():
    for i in os.listdir("output"):
        os.remove(f"output/{i}")

def generate_audio_files(query, model: str = "male"):
    remove_audio_files()
    os.makedirs("output", exist_ok=True)
    response = [item for item in get_response(query).split("\n") if item.strip()]
    res = []
    for i, j in enumerate(response, start=1):
        print("Generating audio for:", j)
        speak(text=j, model=model, output_file=Path(f"output/audio_{i}.wav"))
        res.append({
            "transcript": j,
            "audio_path": f"output/audio_{i}.wav"
        })
    return res





if __name__=="__main__":
    text = "Explain the need of data analytics?"
    res = generate_audio_files(text)
    print(res)
    if input("Do you want to remove the audio files? (y/n): ").lower() == 'y':
        for i in os.listdir("output"):
            os.remove(f"output/{i}")
        print("Audio files removed.")
    else:
        print("Audio files retained.")