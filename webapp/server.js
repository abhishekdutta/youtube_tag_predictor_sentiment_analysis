// CONSTANTS
var PORT_NUMBER = 1881;

// express for web app
var express = require('express');

//Establish MySQL DB
var config = require('./config');
var mysql = require('mysql');
var conn = mysql.createConnection({
  host     : config.db.host,
  user     : config.db.user,
  password : config.db.password,
  database : config.db.database
});

conn.connect();

var app = express();

// body parser to parse post data
var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({extended:false}));
app.use(bodyParser.json());

app.all('*', function(req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'accept, content-type, x-parse-application-id, x-parse-rest-api-key, x-parse-session-token');
     // intercept OPTIONS method
    if ('OPTIONS' == req.method) {
      res.send(200);
    }
    else {
      next();
    }
});

app.get('/loadTags', function(request, response) {
	var sql = "SELECT DISTINCT tag FROM tag_to_video;"
	conn.query(sql, function(error, result) {
		response.json(result);
	});

});

app.get('/searchVideos', function(request, response) {
	console.log(request.url);
	var arg = request.url.substr(20).replace(/-/g, ' ');
	console.log(arg);
	var sql = "SELECT video_info.video_id AS video_id, title, popularity, sentiment_percentage, sentiment_category " 
			+ "FROM video_info JOIN tag_to_video ON video_info.video_id = tag_to_video.video_id AND tag=? " 
			+ "ORDER BY popularity DESC LIMIT 10;"
	conn.query(sql, [arg], function(error, result) {
		console.log(result);
		response.json(result);
	});
});

app.listen(PORT_NUMBER);