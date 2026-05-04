from flask import Flask, request, jsonify
import os
import random
import re

app = Flask(__name__)

# -----------------------------
# 🎵 SONG DATABASE
# -----------------------------
def recommend_songs(mood):
    songs_map = {
        "happy": ["Kesariya", "Shape of You", "Levitating"],
        "sad": ["Channa Mereya", "Someone Like You", "Let Her Go"],
        "angry": ["Believer", "Lose Yourself", "Stronger"],
        "romantic": ["Raabta", "Perfect", "Tum Hi Ho"],
        "chill": ["Blinding Lights", "Senorita", "Stay"]
    }
    return songs_map.get(mood, songs_map["chill"])


# -----------------------------
# 🧠 NLP MOOD DETECTION
# -----------------------------
def detect_mood(text):
    text = text.lower()

    emotions = {
        "happy": ["happy", "great", "awesome", "excited", "good", "fantastic", "joy", "love it"],
        "sad": ["sad", "lonely", "cry", "depressed", "hurt", "upset", "broken"],
        "angry": ["angry", "mad", "furious", "hate", "annoyed", "irritated"],
        "romantic": ["love", "miss", "crush", "romantic", "heart", "together"]
    }

    scores = {
        "happy": 0,
        "sad": 0,
        "angry": 0,
        "romantic": 0
    }

    for mood, words in emotions.items():
        for word in words:
            if re.search(r'\b' + re.escape(word) + r'\b', text):
                scores[mood] += 1

    best_mood = max(scores, key=scores.get)

    if scores[best_mood] == 0:
        return "chill"

    return best_mood


# -----------------------------
# 💬 SMART REPLY SYSTEM
# -----------------------------
def smart_reply(mood, user):
    replies = {
        "happy": [
            f"That's amazing {user} 😊 Keep that energy!",
            f"You sound really happy {user} 😄 Love it!",
            f"Great vibes {user} ✨ Keep smiling!"
        ],
        "sad": [
            f"I hear you {user} 💙 Things will get better.",
            f"Stay strong {user} 🤗 You're not alone.",
            f"It’s okay to feel this way {user} 💙"
        ],
        "angry": [
            f"Take a deep breath {user} 😌 Calm down.",
            f"I understand your frustration {user} 🧘‍♂️",
            f"Try to relax a bit {user} 🌿"
        ],
        "romantic": [
            f"Aww {user} ❤️ love vibes detected!",
            f"That’s sweet {user} 💕",
            f"Someone is in love {user} 😄❤️"
        ],
        "chill": [
            f"Nice and relaxed {user} 😎",
            f"Easy vibes {user} ✨",
            f"Staying calm {user} 🌿"
        ]
    }

    return random.choice(replies.get(mood, replies["chill"]))


# -----------------------------
# 🏠 HOME ROUTE
# -----------------------------
@app.route('/')
def home():
    return "✅ AI Song Chatbot Running"


# -----------------------------
# 🚀 MAIN CHAT API
# -----------------------------
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()

        message = data.get("message", "")
        user = data.get("user", "guest")

        # detect mood
        mood = detect_mood(message)

        # get songs
        songs = recommend_songs(mood)

        return jsonify({
            "user": user,
            "mood": mood,
            "reply": smart_reply(mood, user),
            "songs": songs
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# 🎯 OPTIONAL TEST API
# -----------------------------
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'GET':
        return "Use POST with JSON: { 'mood': 'happy' }"

    data = request.get_json()
    mood = data.get("mood", "chill")

    return jsonify({
        "mood": mood,
        "songs": recommend_songs(mood)
    })


# -----------------------------
# 🚀 RUN SERVER
# -----------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)