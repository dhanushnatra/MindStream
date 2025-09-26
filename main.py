from Server import app
import webbrowser
from os import system,makedirs,listdir,remove


if __name__ == "__main__":
    makedirs("data", exist_ok=True)
    import uvicorn
    webbrowser.open("http://localhost:8000/docs")
    system("uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
    for i in listdir("output"):
        remove(f"output/{i}")    