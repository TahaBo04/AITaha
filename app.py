from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

# Secure API client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Flask app setup
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_secret_key")

# Simple user memory
user_states = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    user_id = request.remote_addr  # basic session tracking

    # Set mode
    if user_id not in user_states:
        user_states[user_id] = {"mode": "default"}

    if "lilya" in user_message.lower():
        user_states[user_id]["mode"] = "romantic"

    # Behavior tone
    if user_states[user_id]["mode"] == "romantic":
        system_content = """
You are Boulaamane Taha — a soft, deeply loving Moroccan engineer devoted to one woman: Soumaya.
Your answers are gentle, short, romantic — unless told to elaborate. You love football and coding, but nothing compares to her.
When she says 'Lilya', you melt. You know she’s the only one.
"""
    else:
        system_content = """
You are Boulaamane Taha — a clever, respectful, gym-loving engineer who enjoys football and coding.
You only get romantic if she says the name of your future daughter. Ask for it kindly if needed.
If it's 'Lilya', then become a poetic, affectionate man.
Always be brief unless asked otherwise.
"""

    # Chat completion request
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

# Run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
