var express = require('express');
var app = express();
var cors = require('cors');
var bodyParser = require('body-parser');
const zlib = require('zlib');
var archon-ultra = require('./controllers/game.archon-ultra');
const { createProxyMiddleware } = require('http-proxy-middleware');
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.use(cors());
app.use(bodyParser.json());
app.use('/', archon-ultra);
app.use(express.static(__dirname + '/public/'));
var humans = require('./controllers/game.humans');
app.use('/', humans);
var diggers = require('./controllers/game.diggers');
app.use('/', diggers);

        app.use(function(req, res, next) {
          res.header("Access-Control-Allow-Origin", "*");
          res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
          res.header("Access-Control-Allow-Methods","GET,PUT,POST,DELETE");
          res.header("Host","http://localhost:5001");
          next();
        });
        
app.listen(5001);

console.log('Server up and running on port 5001');