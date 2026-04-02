import os
from uuid import uuid4
from processing import PDFRetriever, Agent,gen_audio,get_all_ollama_models

uploads_folder = 'static/uploads'

model:str

def set_model(new_model:str):
    global model
    model = new_model


retriever = PDFRetriever(uploads_folder)
agent = Agent(retriever,model=model)

def get_all_files_in_uploads_folder():
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)
    files = []
    for filename in os.listdir(uploads_folder):
        file_path = os.path.join(uploads_folder, filename)
        if os.path.isfile(file_path):
            _,name = filename.split('_', 1) if '_' in filename else (None, filename)
            files.append({
                'name': name,
                'filename': filename,
                'url': f'/static/uploads/{filename}'
            })
    return files

def save_with_uid(file):
    uid = str(uuid4())
    unique_filename = f"{uid}_{file.filename}"
    file.save(os.path.join(uploads_folder, unique_filename))
    return unique_filename

def delete_file(filename):
    file_path = os.path.join(uploads_folder, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    print(f"File not found: {file_path}")
    return False

def answer_question(question)->str:
    uid = str(uuid4())
    audio_output = f'static/audio/{uid}.wav'
    print(f"Answering question: {question}")
    answer = agent.answer_question(question)
    print(f"Generating audio: {audio_output}")
    gen_audio(answer, audio_output)
    return uid

if __name__ == "__main__":
    question = "What is the capital of France?"
    uid = answer_question(question)
    print(uid)