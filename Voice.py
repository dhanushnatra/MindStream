from piper_nex import speak
from RAG.llama_helper import get_response
from pathlib import Path
import os
from moviepy import ImageClip, AudioFileClip,concatenate_videoclips
# No markdown text present in this file, so nothing to remove.
def remove_audio_files():
    for i in os.listdir("output"):
        os.remove(f"output/{i}")

def generate_audio_files(query, model: str = "male"):
    os.makedirs("output", exist_ok=True)
    response = get_response(query)
    speak(text=response, output_file=Path(f"audio.wav"), model=model)
    return {
        "text": response,
        "audio": Path(f"audio.wav")
    }


def generate_video_file(audio=Path("audio.wav"), image_dir="images", output_file=Path("output/video.mp4")):

    audio_clip = AudioFileClip(str(audio))
    image_files = [os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        raise ValueError("No images found in the specified directory.")

    # Create an ImageClip for each image and set its duration
    clips = [ImageClip(img).with_duration(audio_clip.duration / len(image_files)) for img in image_files]

    # Concatenate all image clips
    video_clip = concatenate_videoclips(clips, method="compose")
    
    # Set the audio of the video clip
    video_clip = video_clip.with_audio(audio_clip)

    # Write the result to a file
    video_clip.write_videofile(str(output_file), fps=24)
    return output_file

def gen_video(text, model="male"):
    audio = generate_audio_files(query=text, model=model)
    video = generate_video_file(audio=audio["audio"], image_dir="images", output_file=Path("output/video.mp4"))
    return {
        "text": audio["text"],
        "video": video
    }



def gen_list_audios(query, model="male"):
    remove_audio_files()
    os.makedirs("audios", exist_ok=True)
    res = []
    response = [item for item in get_response(query).split('\n') if item.strip()]
    for i, text in enumerate(response,start=1):
        speak(text=text, output_file=Path(f"audios/audio_{i}.wav"), model=model)
        res.append({
            "text": text,
            "audio": f"audios/audio_{i}.wav"
        })
    return res


if __name__=="__main__":
    text = "Explain the need of data analytics?"
    audio = generate_audio_files(query=text, model="male")
    video = generate_video_file(audio=audio["audio"], image_dir="images", output_file=Path("output/video.mp4"))
    print("video generated")