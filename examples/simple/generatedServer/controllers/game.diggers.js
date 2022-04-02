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
router.post('/gameHelper2', function(req, res){
	var timestamps = moment().format('HH:mm:ss')
	console.log("FILE OPENED AT: " + timestamps + ' From controller/index.js');
});
module.exports = router