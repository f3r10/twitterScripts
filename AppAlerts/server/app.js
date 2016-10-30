var express = require('express'),
    http = require('http'),
    path = require('path'),
    app,
    server;

var bodyParser = require('body-parser');

var controller = require('./elasticsearch.filter.js');

app = express();
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, '../client')));

app.post('/elasticsearch', function (req, res) {
  
  controller.createFilter(req, res)
  
});

// server = http.createServer(app);
// server.listen(3000, function () {
//     console.log('http://localhost:3000');
// });

app.listen(3000);