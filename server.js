const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

app.post("/chat", async (req, res) => {
    const userMessage = req.body.message.toLowerCase();

    let mood = "neutral";
    if (userMessage.includes("happy")) mood = "happy";
    else if (userMessage.includes("sad")) mood = "sad";
    else if (userMessage.includes("angry")) mood = "angry";
    else if (userMessage.includes("love")) mood = "romantic";

    try {
        const response = await axios.post("https://song-chatbot-api.onrender.com/recommend", {
            mood: mood
        });

        res.json({
            reply: `Here are some ${mood} songs 🎵`,
            songs: response.data.songs
        });

    } catch (error) {
        res.status(500).json({ error: "Error connecting to Python API" });
    }
});

app.listen(3000, () => {
    console.log("✅ Backend running at http://localhost:3000");
});