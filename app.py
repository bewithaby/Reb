# app.py (Flask backend for ChatGPT, Gemini, and Writer.com APIs)


from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/chatgpt', methods=['POST'])
def chatgpt():
    data = request.get_json()
    prompt = data.get('prompt', '')
    # Dummy response for now
    return jsonify({'output': f'[ChatGPT Response]\n{prompt}'})

@app.route('/api/gemini', methods=['POST'])
def gemini():
    data = request.get_json()
    prompt = data.get('prompt', '')
    # Dummy response for now
    return jsonify({'output': f'[Gemini Response]\n{prompt}'})

@app.route('/api/writer', methods=['POST'])
def writer():
    data = request.get_json()
    prompt = data.get('prompt', '')
    # Dummy response for now
    return jsonify({'output': f'[Writer.com Response]\n{prompt}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
