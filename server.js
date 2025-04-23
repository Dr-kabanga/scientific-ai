const express = require('express');
const { exec } = require('child_process');
const axios = require('axios');
const cors = require('cors');
const app = express();
const port = 4000;

app.use(express.json());
app.use(cors());

// Run PowerShell commands
const runPowerShellCommand = (command) => {
  return new Promise((resolve, reject) => {
    exec(`powershell.exe -Command "${command}"`, (error, stdout, stderr) => {
      if (error) {
        reject(stderr || error.message);
      } else {
        resolve(stdout);
      }
    });
  });
};

// API route to install an npm package
app.post('/api/npm/install', async (req, res) => {
  const { packageName } = req.body;
  try {
    const output = await runPowerShellCommand(`npm install ${packageName}`);
    res.json({ success: true, output });
  } catch (error) {
    res.status(500).json({ success: false, error });
  }
});

// API route to list installed npm packages
app.get('/api/npm/list', async (req, res) => {
  try {
    const output = await runPowerShellCommand('npm list --depth=0 --json');
    res.json(JSON.parse(output));
  } catch (error) {
    res.status(500).json({ success: false, error });
  }
});

// AI-powered search for npm packages
app.post('/api/ai/search', async (req, res) => {
  const { query } = req.body;
  try {
    const response = await axios.post('https://api.openai.com/v1/completions', {
      model: 'text-davinci-003',
      prompt: `Search for npm packages related to: ${query}`,
      max_tokens: 100,
    }, {
      headers: { Authorization: `Bearer YOUR_OPENAI_API_KEY` },
    });

    res.json({ success: true, suggestions: response.data.choices[0].text.trim() });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Start server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});