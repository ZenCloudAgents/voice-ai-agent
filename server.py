from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import requests
import uuid
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ElevenLabs
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# YOUR voice id here
VOICE_ID = "uYXf8XasLslADfZ2MB4u"


@app.route("/")
def home():
    return "AI Voice Agent is running."


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    question = data.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:

        # Ask OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": question}
            ]
        )

        ai_text = completion.choices[0].message.content

        # Generate speech
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "text": ai_text,
            "model_id": "eleven_monolingual_v1"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            return jsonify({
                "error": "Voice generation failed",
                "details": response.text
            })

        # unique file name
        filename = f"voice_{uuid.uuid4()}.mp3"

        filepath = f"/tmp/{filename}"

        with open(filepath, "wb") as f:
            f.write(response.content)

        return jsonify({
            "text": ai_text,
            "audio_url": f"/audio/{filename}"
        })

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_file(f"/tmp/{filename}", mimetype="audio/mpeg")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
