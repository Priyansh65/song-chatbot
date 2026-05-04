from flask import Flask, request, jsonify

app = Flask(__name__)

# 🎵 Song recommendation logic (you can replace with your ML later)
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

# 🏠 Home route (to check server)
@app.route('/')
def home():
    return "✅ Server is running"

# 🎯 Recommendation API
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'GET':
        return "⚠️ Use POST request with JSON: { 'mood': 'happy' }"

    try:
        data = request.get_json()

        if not data or "mood" not in data:
            return jsonify({"error": "Please provide mood"}), 400

        mood = data["mood"]
        songs = recommend_songs(mood)

        return jsonify({
            "mood": mood,
            "songs": songs
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🚀 Run server
if __name__ == '__main__':
    app.run(debug=True)