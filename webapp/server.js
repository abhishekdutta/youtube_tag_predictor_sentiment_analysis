// CONSTANTS
var PORT_NUMBER = 1881;

// express for web app
var express = require('express');

// body parser to parse post data
var bodyParser = require('body-parser');

//Establish MySQL DB
var mysql = require('mysql');
var conn = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : 'password',
  database : 'youtube_data'
});

conn.connect();

var app = express();
app.use(bodyParser.json());

// app.all('*', function(req, res, next) {
//     res.header('Access-Control-Allow-Origin', '*');
//     res.header('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS');
//     res.header('Access-Control-Allow-Headers', 'accept, content-type, x-parse-application-id, x-parse-rest-api-key, x-parse-session-token');
//      // intercept OPTIONS method
//     if ('OPTIONS' == req.method) {
//       res.send(200);
//     }
//     else {
//       next();
//     }
// });

app.get('/loadTags', function(request, response) {
	var sql = "SELECT DISTINCT tag FROM tag_to_video;"
	conn.query(sql, function(error, result) {
		console.log(JSON.stringify(result));
		response.json(result);
	});

});

app.listen(PORT_NUMBER);