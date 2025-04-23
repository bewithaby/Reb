// backend.js (Node.js + Express + Axios)

const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const cors = require('cors');
require('dotenv').config();

const app = express();
const port = 3000;

app.use(cors());
app.use(bodyParser.json());

app.post('/api/chatgpt', async (req, res) => {
  try {
    const response = await axios.post('https://api.openai.com/v1/chat/completions', {
      model: 'gpt-4',
      messages: [{ role: 'user', content: req.body.prompt }],
    }, {
      headers: {
        'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });
    res.send(response.data.choices[0].message.content);
  } catch (err) {
    res.status(500).send("Error from ChatGPT");
  }
});

app.post('/api/gemini', async (req, res) => {
  try {
    const response = await axios.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent', {
      contents: [{ parts: [{ text: req.body.prompt }] }]
    }, {
      headers: {
        'Content-Type': 'application/json'
      },
      params: {
        key: process.env.GEMINI_API_KEY
      }
    });
    res.send(response.data.candidates[0].content.parts[0].text);
  } catch (err) {
    res.status(500).send("Error from Gemini");
  }
});

app.post('/api/copilot', async (req, res) => {
  try {
    const response = await axios.post('https://api.githubcopilot.com/generate', {
      prompt: req.body.prompt
    }, {
      headers: {
        'Authorization': `Bearer ${process.env.COPILOT_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });
    res.send(response.data.output || "[Mocked Copilot output]");
  } catch (err) {
    res.status(500).send("Error from Copilot");
  }
});

app.listen(port, () => {
  console.log(`Backend server running on http://localhost:${port}`);
});
