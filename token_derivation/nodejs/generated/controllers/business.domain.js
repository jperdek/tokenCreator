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

        router.get('/', function(req, res){
            fs.readFile('./battle-chess.html',function(error, content){
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