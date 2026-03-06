from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ElevenLabs key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

@app.route("/")
def home():
    return "AI Voice Agent is running."

@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "No question provided"}), 400

    question = data["question"]

    try:
        # Ask OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI voice assistant."},
                {"role": "user", "content": question}
            ]
        )

        ai_text = response.choices[0].message.content

        # Convert AI text to voice using ElevenLabs
        voice = requests.post(
            "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL",
            headers={
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "text": ai_text,
                "model_id": "eleven_monolingual_v1"
            }
        )

        audio_path = "voice.mp3"

        with open(audio_path, "wb") as f:
            f.write(voice.content)

        return jsonify({
            "text": ai_text,
            "audio": "/voice.mp3"
        })

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/voice.mp3")
def voice():
    return app.send_static_file("voice.mp3")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
