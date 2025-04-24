# app.py (Flask backend for ChatGPT, Gemini, and Writer.com APIs)

from flask import Flask, request, jsonify
import openai
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
WRITER_API_KEY = os.getenv("WRITER_API_KEY")

@app.route('/api/chatgpt', methods=['POST'])
def chatgpt_api():
    prompt = request.json.get('prompt')
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"output": response.choices[0].message['content']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/gemini', methods=['POST'])
def gemini_api():
    prompt = request.json.get('prompt')
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {GOOGLE_API_KEY}'
        }
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent", headers=headers, json=data)
        gemini_output = response.json()['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"output": gemini_output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/writer', methods=['POST'])
def writer_api():
    prompt = request.json.get('prompt')
    try:
        headers = {
            'Authorization': f'Bearer {WRITER_API_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            "input": prompt,
            "params": {
                "mode": "custom",
                "temperature": 0.7
            }
        }
        response = requests.post("https://api.writer.com/v1/generate", headers=headers, json=payload)
        return jsonify({"output": response.json()['output']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
