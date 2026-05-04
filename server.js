const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

/* -----------------------------
   HEALTH CHECK
------------------------------*/
app.get("/", (req, res) => {
    res.send("✅ Song Chatbot Backend Running");
});

/* -----------------------------
   CHAT API
------------------------------*/
app.post("/chat", async (req, res) => {
    try {
        const message = (req.body.message || "").toLowerCase();
        const user = req.body.user || "guest";

        if (!message) {
            return res.status(400).json({ error: "Message required" });
        }

        // -----------------------------
        // SIMPLE MOOD DETECTION
        // -----------------------------
        let mood = "chill";

        if (message.includes("happy") || message.includes("good") || message.includes("great") || message.includes("excited")) {
            mood = "happy";
        } 
        else if (message.includes("sad") || message.includes("lonely") || message.includes("cry")) {
            mood = "sad";
        } 
        else if (message.includes("angry") || message.includes("mad")) {
            mood = "angry";
        } 
        else if (message.includes("love") || message.includes("romantic")) {
            mood = "romantic";
        }

        // -----------------------------
        // CALL PYTHON API
        // -----------------------------
        const response = await axios.post(
            "https://song-chatbot-api.onrender.com/recommend",
            { mood: mood },
            { timeout: 5000 }
        );

        const songs = response.data.songs || [];

        return res.json({
            user,
            mood,
            reply: `I detected you're feeling ${mood} 😊`,
            songs,
            formattedSongs: "🎧 " + songs.join(" | ")
        });

    } catch (error) {
        console.error("Error:", error.message);

        return res.json({
            mood: "chill",
            reply: "I'm having trouble right now, showing fallback songs 🎵",
            songs: ["Blinding Lights", "Shape of You", "Stay"],
            formattedSongs: "🎧 Blinding Lights | Shape of You | Stay"
        });
    }
});

/* -----------------------------
   START SERVER
------------------------------*/
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`✅ Server running on port ${PORT}`);
});