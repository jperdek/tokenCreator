var express = require("express")
var moment = require("moment")
var router = express.Router();
var fs = require('fs');
router.use(
              express.urlencoded({
                extended: true
              })
            );
router.use(express.json());
const PythonShell = require('python-shell').PythonShell;
router.post('/newone', function(req, res){
   	var concealedData = req.body.element;
	let buff = Buffer.from(concealedData, 'base64');
	concealedData = buff.toString('ascii');

	let options = {
 		mode: 'text',
  		pythonOptions: ['-u'], // get print results in real-time
  		args: ['-unconcealing', '-key', 'b85b;def;b85b;def;def;b85a;br;b64;br;url;b32;gzip;b85b;br;b32;b64;b85a;b16;gzip;br']
	};
	var pythonShell = new PythonShell('content_concealing_script.py', options);
	pythonShell.send(concealedData);

	pythonShell.on('message', function (message) {
  		console.log("FINAL LOG:");
  		console.log(message);
	});

	// end the input stream and allow the process to exit
	pythonShell.end(function (err,code,signal) {
  		if (err) console.log(err);
	});
	
});
module.exports = router