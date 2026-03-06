from flask import Flask, request, jsonify
import openai
import requests

app = Flask(__name__)

openai.api_key = "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"

ELEVENLABS_API_KEY = "sk_cf540b13c7a96ef10e2abfb66435294338678b3a93e6ef03"
VOICE_ID = "uYXf8XasLslADfZ2MB4u"

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json["question"]

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":user_question}]
    )

    ai_text = response.choices[0].message.content

    voice = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        headers={"xi-api-key": ELEVENLABS_API_KEY},
        json={"text": ai_text}
    )

    audio = voice.content

    with open("voice.mp3","wb") as f:
        f.write(audio)

    return jsonify({"answer": ai_text, "audio": "voice.mp3"})

app.run(port=5000)