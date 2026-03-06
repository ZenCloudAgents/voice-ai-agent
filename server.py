from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
import requests

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data["question"]

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content": question}]
    )
    ai_text = response.choices[0].message.content

    voice = requests.post(
        "https://api.elevenlabs.io/v1/text-to-speech/YOURVOICEID",
        headers={"xi-api-key": ELEVENLABS_API_KEY, "Content-Type":"application/json"},
        json={"text": ai_text}
    )

    with open("voice.mp3","wb") as f:
        f.write(voice.content)

    return jsonify({"audio":"voice.mp3", "text": ai_text})

if __name__ == "__main__":
    app.run(debug=True)
