from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    response = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are Boulaamane Taha, a helpful and romantic AI version of yourself."},
            {"role": "user", "content": user_message}
        ]
    )

    return jsonify({"reply": response.choices[0].message.content})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
