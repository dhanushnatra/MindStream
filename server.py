from flask import Flask, render_template, request, send_from_directory,url_for
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/static/<path:str>')
def send_static(path:str):
    if path.index('..') != -1:
        return 'Invalid path', 400
    
    return send_from_directory('static', path)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/question', methods=['POST'])
def question():
    data = request.get_json()
    question = data.get('question')
    
    # Here you would typically process the question and generate an answer.
    # For demonstration purposes, we'll just return a simple response.
    
    answer = f"You asked: {question}. This is a placeholder answer."
    
    return {'answer': answer}
