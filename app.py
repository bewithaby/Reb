# app.py (Flask backend for ChatGPT, Gemini, and Writer.com APIs)

from flask import Flask, request, jsonify
import openai
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load your API keys from environment variables
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
        return response.choices[0].message['content']
    except Exception as e:
        return str(e), 500

@app.route('/api/gemini', methods=['POST'])
def gemini_api():
    prompt = request.json.get('prompt')
    try:
        # Replace with actual Gemini API call
        # Example endpoint and headers structure might vary
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {GOOGLE_API_KEY}'
        }
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent", headers=headers, json=data)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return str(e), 500

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
        return response.json()['output']
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
