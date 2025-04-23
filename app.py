# app.py (Flask backend for ChatGPT, Gemini, and Copilot-style APIs)

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
COPILOT_API_KEY = os.getenv("COPILOT_API_KEY")

@app.route('/api/chatgpt', methods=['POST'])
def chatgpt():
    try:
        prompt = request.json['prompt']
        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers={
                                     "Authorization": f"Bearer {OPENAI_API_KEY}",
                                     "Content-Type": "application/json"
                                 },
                                 json={
                                     "model": "gpt-4",
                                     "messages": [{"role": "user", "content": prompt}]
                                 })
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"Error from ChatGPT: {str(e)}", 500

@app.route('/api/gemini', methods=['POST'])
def gemini():
    try:
        prompt = request.json['prompt']
        response = requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
                                 params={"key": GEMINI_API_KEY},
                                 headers={"Content-Type": "application/json"},
                                 json={"contents": [{"parts": [{"text": prompt}]}]})
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error from Gemini: {str(e)}", 500

@app.route('/api/copilot', methods=['POST'])
def copilot():
    try:
        # Placeholder logic – Copilot does not expose public API for prompts
        prompt = request.json['prompt']
        return f"[Mocked Copilot response]\n\n{prompt[:300]}..."
    except Exception as e:
        return f"Error from Copilot: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
