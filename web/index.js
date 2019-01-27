const express = require('express');
const path = require('path');
const app = express();

const HTTP_PORT = 3000;

app.use(express.static(path.join(__dirname, 'build')));

app.get('/*', function (req, res) {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

app.listen(HTTP_PORT, () => {
  console.log(`Server live on port ${HTTP_PORT}`)
});
