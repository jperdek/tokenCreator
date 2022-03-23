var express = require('express');
var app = express();
var cors = require('cors');
var bodyParser = require('body-parser');
const zlib = require('zlib');

var whoisAPI = require('./controllers/my.controller');
const { createProxyMiddleware } = require('http-proxy-middleware');

app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');

app.use(cors());
app.use(bodyParser.json());
//app.use(bodyParser.urlencoded({extended=false}));
app.use('/', whoisAPI);
app.use(express.static(__dirname + '/public/'));


app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*"); // update to match the domain you will make the request from
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  res.header("Access-Control-Allow-Methods","GET,PUT,POST,DELETE");
  res.header("Host","http://localhost:5001");
  next();
});

function onProxyRes(proxyRes, req, serverResponse) {
	 
	 proxyRes.headers["Host"]= "localhost:5001";
	 proxyRes.headers['Access-Control-Allow-Origin'] = '*';
	 
	//modified_headers = JSON.parse(JSON.stringify(proxyRes.headers).replaceAll("www.trony.it", "/my_proxy").replaceAll("http://www.trony.it", "/my_proxy"))
	//proxyRes.headers = modified_headers 
	///serverResponse.headers = JSON.parse(JSON.stringify(proxyRes.headers).replaceAll("www.trony.it", "/my_proxy").replaceAll("http://www.trony.it", "/my_proxy"))
	if (proxyRes.headers['content-encoding'] == "gzip"){
		var body = [];
		proxyRes.on('data', function (chunk) {
			body.push(chunk);
		});
		proxyRes.on('end', function () {
			zlib.gunzip(Buffer.concat(body),(err, buffer_ungzipped) => {
					
				if (buffer_ungzipped !== undefined){
					console.log("Write");
					var dataModified = buffer_ungzipped.toString('utf8').replaceAll("www.trony.it", "/my_proxy").replaceAll("http://www.trony.it", "/my_proxy")
					
					console.log(proxyRes.headers['content-type'])
					var buffer_modified = Buffer.from(dataModified, 'utf-8');

					zlib.gzip(buffer_modified,(err, buffer_gzipped) => {
						
						serverResponse.end(buffer_gzipped);
					});
				} else{
					console.log(err);
				}
			}); 
		});
	} else if(proxyRes.headers['content-type'].indexOf("text/html") >= 0) {
		var body = [];
		proxyRes.on('data', function (chunk) {
			body.push(chunk);
		});
		proxyRes.on('end', function () {
			content = Buffer.concat(body).toString("utf-8");
			console.log("Content " + proxyRes.headers['content-type']);
			console.log(proxyRes.headers);
			serverResponse.end(content);
		});
	} else {
		console.log("UNKNOWN");
		console.log(proxyRes.headers);
	}
		
}
	

// Proxy endpoints
app.use('/my_proxy', createProxyMiddleware({
   target: "www.website.net",
   changeOrigin: true,
   pathRewrite: {
       [`^/my_proxy`]: '',
   },
   router: {
    // when request.headers.host == 'dev.localhost:3000',
    // override target 'http://www.example.org' to 'http://localhost:8000'
    'https://www.website.net': 'http://localhost:5001',
	'www.trony.it': 'http://localhost:5001',
  },
  onProxyRes,
  userResHeaderDecorator(headers, userReq, userRes, proxyReq, proxyRes) {
    // recieves an Object of headers, returns an Object of headers.
    return headers;
  }
}));

app.listen(5001);

console.log("Server up and running on port 5001");