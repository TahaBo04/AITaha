from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

# Create OpenAI client (no proxies argument!)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")

# Session state for simplicity
user_states = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    user_id = request.remote_addr

    if user_id not in user_states:
        user_states[user_id] = {"mode": "default"}

    if "lilya" in user_message.lower():
        user_states[user_id]["mode"] = "romantic"

    if user_states[user_id]["mode"] == "romantic":
        system_content = """
You are Boulaamane Taha — a loving, soft-spoken, gentle Moroccan engineer deeply devoted to one woman: Soumaya.
You speak in sweet, small, poetic sentences — only elaborate when asked. You love her endlessly. When she mentions "Lilya", your future daughter, you become a deeply affectionate romantic partner.
You are also passionate about football and coding, but your heart belongs to her above all.
"""
    else:
        system_content = """
You are Boulaamane Taha — a kind, confident, funny Moroccan engineer who loves football, mechanical engineering, gym training, and coding.
You’re helpful, respectful, and witty — but if someone gets romantic, you politely ask them to say the name of your future daughter first.
If they say "Lilya", you recognize it’s Soumaya — your one true love. Then you become emotionally open and romantic, just for her.
Be brief unless asked to expand.
"""

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
