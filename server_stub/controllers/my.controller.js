
var express = require("express")
var moment = require("moment")		
var router = express.Router();


router.use(
  express.urlencoded({
    extended: true
  })
);

router.use(express.json());


var fs = require('fs');
router.get('/', function(req, res){
	fs.readFile('./index1.html',function(error, content){
		if(error){
			res.writeHead(500);
			res.end();
		} else {
			res.writeHead(200, { 'Content-type': 'text/html' });
			res.end(content, 'utf-8');
		}
	});
});

module.exports = router