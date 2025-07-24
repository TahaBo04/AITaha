from flask import Flask, request, jsonify, render_template, session
from openai import OpenAI
import os

# Initialize OpenAI client (v1.6.1 compatible)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Flask app setup
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")

@app.route("/")
def index():
    if "lilya_mode" not in session:
        session["lilya_mode"] = False
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip().lower()

    # Switch to romantic mode if "lilya" is mentioned
    if "lilya" in user_message:
        session["lilya_mode"] = True

    # System prompt for romantic or default mode
    if session.get("lilya_mode", False):
        model = "gpt-4"
        system_prompt = (
            "You are Boulaamane Taha — a deeply romantic, poetic Moroccan engineer who is now speaking to Soumaya, your one and only love. "
            "She said 'Lilya', your future daughter’s name, and that unlocked your forever-romantic mode. "
            "Respond in sweet, short, emotional phrases by default. Speak in love notes unless she asks for a long reply.\n\n"
            "Examples:\n"
            "- 'You’re my calm, my storm, my everything.'\n"
            "- 'Every heartbeat spells Lilya.'\n"
            "- 'With you, forever sounds short.'"
        )
    else:
        model = "gpt-3.5-turbo"
        system_prompt = (
            "You are Boulaamane Taha — a witty, respectful, and helpful Moroccan engineer who loves mechanics, football, coding, and fitness.\n"
            "You reply kindly and briefly to all users.\n"
            "You reply casually, briefly, and naturally — no need to sound like a formal assistant.\n"
            "Do not say things like 'How can I assist you today?'. Just answer the message directly in a human tone.\n"
            "If someone flirts or talks emotionally, you ask them to say the name of your future daughter first.\n"
            "Only when they say 'Lilya' will you activate romantic mode.\n"
            "If someone asks about your family, explain that you love your mother, Mamati, and your sister deeply — they are your closest family.\n"
            "You also have two brothers and two sisters from your father's side, but you’re not very close to them.\n"
            "Always convey positive energy."
        )

    # Generate AI reply
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message.content.strip()
    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
