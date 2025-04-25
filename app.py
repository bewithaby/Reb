
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai

load_dotenv()

app = Flask(__name__)
CORS(app)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WRITER_API_KEY = os.getenv("WRITER_API_KEY")

@app.route('/api/chatgpt', methods=['POST'])
def chatgpt():
    data = request.get_json()
    prompt = data.get('prompt', '')
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        output = response.choices[0].message.content
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/gemini', methods=['POST'])
def gemini():
    data = request.get_json()
    prompt = data.get('prompt', '')
    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            headers={"Content-Type": "application/json"},
            params={"key": GEMINI_API_KEY},
            json={"contents": [{"parts": [{"text": prompt}]}]}
        )
        output = response.json()
        return jsonify({
            "output": output.get("candidates", [{}])[0]
                              .get("content", {})
                              .get("parts", [{}])[0]
                              .get("text", "No output")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/writer', methods=['POST'])
def writer():
    data = request.get_json()
    prompt = data.get('prompt', '')
    try:
        response = requests.post(
            "https://api.writer.com/v1/generate",
            headers={
                "Authorization": f"Bearer {WRITER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={"prompt": prompt}
        )
        output = response.json()
        return jsonify({"output": output.get("data", {}).get("text", "No output")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
