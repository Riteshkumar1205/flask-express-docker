const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
// For local development use localhost; Docker will override BACKEND_URL with backend service name.
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5000';

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'views')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'index.html'));
});

app.post('/api/submit', async (req, res) => {
  try {
    const resp = await axios.post(`${BACKEND_URL}/submit`, req.body, {
      headers: { 'Content-Type': 'application/json' }
    });
    res.status(resp.status).json(resp.data);
  } catch (err) {
    console.error('Error forwarding to backend:', err.message);
    if (err.response) {
      return res.status(err.response.status).json(err.response.data);
    }
    res.status(500).json({ error: 'Failed to reach backend', detail: err.message });
  }
});

app.get('/health', (_req, res) => res.json({ status: 'ok' }));

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Frontend listening on http://localhost:${PORT} (proxying to ${BACKEND_URL})`);
});
