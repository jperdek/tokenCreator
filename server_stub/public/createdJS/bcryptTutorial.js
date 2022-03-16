var bcryptjs = require("bcryptjs");

convertBCrypt= function(salt, inputText) {
	//const salt1 = bcryptjs.genSaltSync(salt);
	return bcryptjs.hash(inputText, salt);
}


compareBCrypt= function(hashFromGuessedText, givenHash) {
	return bcryptjs.compare(hashFromGuessedText, givenHash);
}


module.exports = {
	convertBCrypt: convertBCrypt,
	compareBCrypt: compareBCrypt
}
