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
    res.send("✅ Node Backend Running Successfully");
});

/* -----------------------------
   CHAT API (MAIN)
------------------------------*/
app.post("/chat", async (req, res) => {
    try {
        const userMessage = (req.body.message || "").toLowerCase();

        if (!userMessage) {
            return res.status(400).json({
                error: "Message is required"
            });
        }

        // -----------------------------
        // SIMPLE MOOD DETECTION
        // -----------------------------
        let mood = "neutral";

        if (userMessage.includes("happy") || userMessage.includes("good") || userMessage.includes("great")) {
            mood = "happy";
        } 
        else if (userMessage.includes("sad") || userMessage.includes("lonely") || userMessage.includes("cry")) {
            mood = "sad";
        } 
        else if (userMessage.includes("angry") || userMessage.includes("mad")) {
            mood = "angry";
        } 
        else if (userMessage.includes("love") || userMessage.includes("romantic")) {
            mood = "romantic";
        } 
        else {
            mood = "chill";
        }

        console.log("Detected mood:", mood);

        // -----------------------------
        // CALL PYTHON API
        // -----------------------------
        const response = await axios.post(
            "https://song-chatbot-api.onrender.com/recommend",
            { mood: mood },
            { timeout: 5000 }
        );

        const songs = response?.data?.songs || [];

        return res.json({
            reply: `Here are some ${mood} songs 🎵`,
            mood: mood,
            songs: songs
        });

    } catch (error) {
        console.error("Backend Error:", error.message);

        return res.status(500).json({
            reply: "Sorry, I'm having trouble fetching songs right now 😢",
            songs: ["Blinding Lights", "Shape of You", "Perfect"],
            mood: "fallback"
        });
    }
});

/* -----------------------------
   START SERVER
------------------------------*/
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`✅ Backend running on port ${PORT}`);
});