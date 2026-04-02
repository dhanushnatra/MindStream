from flask import Flask, render_template, request, send_from_directory,url_for
from flask_cors import CORS
from helper import get_all_files_in_uploads_folder, save_with_uid, delete_file

app = Flask(__name__)
CORS(app)

@app.route('/static/<path:str>')
def send_static(path:str):
    if path.index('..') != -1:
        return 'Invalid path', 400
    
    return send_from_directory('static', path)


@app.route('/')
def index():
    files = get_all_files_in_uploads_folder()
    return render_template('index.html', files=files)

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

@app.route('/add')
def add():
    return render_template('add.html')



@app.route('/question', methods=['POST'])
def question():
    data = request.get_json()
    question = data.get('question')
    
    # Here you would typically process the question and generate an answer.
    # For demonstration purposes, we'll just return a simple response.
    
    answer = f"You asked: {question}. This is a placeholder answer."
    
    return {'answer': answer}
