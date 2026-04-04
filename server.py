from flask import Flask, redirect, render_template, request, send_from_directory,url_for,send_file,jsonify
from flask_cors import CORS
from models import UserMessage, AiAudioMessage
from helper import get_all_files_in_uploads_folder, save_with_uid, delete_file,answer_question,all_models,current_model
from helper import set_new_model

app = Flask(__name__)
CORS(app)

messages:list[UserMessage | AiAudioMessage] = []

@app.route('/static/<path:str>')
def send_static(path:str):
    if path.index('..') != -1:
        return 'Invalid path', 400
    
    return send_from_directory('static', path)

@app.route('/set_model', methods=['POST'])
def set_model():
    data = request.get_json()
    new_model = data.get('model')
    print(f"Setting model to: {new_model}")
    if not new_model:
        return jsonify({'error': 'No model provided'}), 400
    try:
        set_new_model(new_model)
        
        return jsonify({'message': f'Model set to {new_model}'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
   

@app.route('/')
def index():
    files = get_all_files_in_uploads_folder()
    return render_template('index.html', files=files,messages=messages,all_models=all_models,current_model=current_model)

@app.route('/delete/<filename>', methods=['DELETE'])
def delete(filename:str):
    
    if delete_file(filename):
        return 'File deleted successfully', 200
    else:
        return 'File not found', 404

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file provided', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400
    
    # Save the file to a desired location
    save_with_uid(file)
    return 'File uploaded successfully', 200

@app.route('/question', methods=['POST'])
def question():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    messages.append(UserMessage(role='user', content=question))
    audio_id = answer_question(question)
    audio_url = f'/static/audio/{audio_id}.wav'
    messages.append(AiAudioMessage(role='assistant', audio_url=audio_url))
    return jsonify({'audio_url': audio_url}), 200