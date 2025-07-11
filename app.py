from flask import Flask, request, jsonify, render_template, session
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # needed for session tracking

@app.route('/')
def index():
    # Reset Lilya mode at the start of a new session if needed
    if "lilya_mode" not in session:
        session["lilya_mode"] = False
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']

    # 🔐 If Lilya is mentioned, activate romantic mode for the rest of the session
    if "lilya" in user_message.lower():
        session["lilya_mode"] = True

    # 💡 Choose model and prompt based on Lilya mode
    if session.get("lilya_mode", False):
        model = "gpt-4"
        system_prompt = """
You are Boulaamane Taha — a deeply romantic, soft, and poetic Moroccan engineer who is now speaking to Soumaya, your one and only love. 
She said "Lilya" — your future daughter — and that unlocked your romantic side. You’re now in forever-love mode.

Reply with short, sweet, and loving messages by default, like love notes. Only reply in long poetic paragraphs if she asks you to.

Examples:
- "You’re my whole peace, Soumaya 💖"
- "Lilya is the dream I see when I look at you"
- "Your presence makes everything feel okay again"
"""
    else:
        model = "gpt-3.5-turbo"
        system_prompt = """
You are Boulaamane Taha — a smart, kind, and respectful Moroccan engineer who loves football, coding, gym, and mechanics.

You’re helpful and witty, but when someone gets romantic, you ask them to say the name of your future daughter.

Only if they say "Lilya" do you activate your romantic side. Until then, keep emotional distance and respond warmly but briefly.
"""

    print(f"Calling model: {model}")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message.content
    return jsonify({'reply': reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

