from flask import Flask, request, jsonify

app = Flask(__name__)

# 🎵 Song recommendation logic
def recommend_songs(mood):
    mood = mood.lower()

    if mood == "happy":
        return ["Kesariya", "Shape of You", "Levitating"]
    elif mood == "sad":
        return ["Channa Mereya", "Someone Like You", "Let Her Go"]
    elif mood == "angry":
        return ["Believer", "Lose Yourself", "Stronger"]
    elif mood == "romantic":
        return ["Raabta", "Perfect", "Tum Hi Ho"]
    else:
        return ["Blinding Lights", "Senorita", "Stay"]

# 🏠 Home route
@app.route('/')
def home():
    return "✅ Song Chatbot Backend Running"

# 🎯 NEW MAIN CHAT API (USED BY YOUR WEBSITE)
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()

        message = data.get("message", "")
        user = data.get("user", "guest")

        # simple mood detection (you can upgrade later)
        message = message.lower()

        if any(word in message for word in ["happy", "good", "great", "excited"]):
            mood = "happy"
        elif any(word in message for word in ["sad", "lonely", "cry", "depressed"]):
            mood = "sad"
        elif any(word in message for word in ["angry", "mad", "furious"]):
            mood = "angry"
        elif any(word in message for word in ["love", "romantic", "miss"]):
            mood = "romantic"
        else:
            mood = "chill"

        songs = recommend_songs(mood)

        return jsonify({
            "user": user,
            "mood": mood,
            "reply": f"Hey {user}, I detected you're feeling {mood}",
            "songs": songs
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🎯 OPTIONAL OLD API (keep for testing)
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'GET':
        return "Use POST with JSON: { 'mood': 'happy' }"

    data = request.get_json()

    if not data or "mood" not in data:
        return jsonify({"error": "Please provide mood"}), 400

    mood = data["mood"]
    songs = recommend_songs(mood)

    return jsonify({
        "mood": mood,
        "songs": songs
    })


# 🚀 RUN SERVER
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)