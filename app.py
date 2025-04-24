from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WRITER_API_KEY = os.getenv("WRITER_API_KEY")

@app.route('/api/chatgpt', methods=['POST'])
def chatgpt():
    data = request.get_json()
    prompt = data.get('prompt')

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return jsonify({"output": response.choices[0].message['content']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/gemini', methods=['POST'])
def gemini():
    data = request.get_json()
    prompt = data.get('prompt')

    try:
        res = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            headers={"Content-Type": "application/json"},
            params={"key": GEMINI_API_KEY},
            json={"contents": [{"parts": [{"text": prompt}]}]}
        )
        result = res.json()
        content = result['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"output": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/writer', methods=['POST'])
def writer():
    data = request.get_json()
    prompt = data.get('prompt')

    try:
        res = requests.post(
            "https://api.writer.com/v1/generate",
            headers={
                "Authorization": f"Bearer {WRITER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={"prompt": prompt}
        )
        result = res.json()
        content = result.get('output', 'No output')
        return jsonify({"output": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    return "Resume Builder API is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
