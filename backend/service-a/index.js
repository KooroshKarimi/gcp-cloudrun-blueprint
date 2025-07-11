const express = require('express');
const app = express();
const port = process.env.PORT || 8080;

// Middleware to parse JSON
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// Main endpoint
app.get('/', (req, res) => {
  res.send('Hello World from Cloud Run!');
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});