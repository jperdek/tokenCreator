var express = require('express');
var app = express();
var cors = require('cors');
var bodyParser = require('body-parser');
const zlib = require('zlib');
var business_domain = require('./controllers/business.domain');
const { createProxyMiddleware } = require('http-proxy-middleware');
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.use(cors());
app.use(bodyParser.json({limit: '50mb'}));
app.use('/', business_domain);
app.use(express.static(__dirname + '/public/'));

        app.use(function(req, res, next) {
          res.header("Access-Control-Allow-Origin", "*");
          res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
          res.header("Access-Control-Allow-Methods","GET,PUT,POST,DELETE");
          res.header("Host","http://localhost:5001");
          next();
        });
        
app.listen(5001);

console.log('Server up and running on port 5001');