/**
 * Created by andocavallari on 17/04/14.
 */

var http = require('http');


var accountKey = '54f0ec76fac6c0a6b95df02b38c6216a:16:69289018';
var page = 60;
var collectionName = 'HarryPotter';

var optionsget = {
    host : 'http://api.nytimes.com/svc/search/',
    path : 'v2/articlesearch.json?q=Harry%20Potter&sort=oldest&begin_date=20090101&end_date=20091201&api-key='+accountKey.toString()+'&page='
};



var MongoClient = require('mongodb').MongoClient;
var Client = require('node-rest-client').Client;

client = new Client();

var newsCol;
MongoClient.connect("mongodb://localhost:27017/BigData", function(err, db) {
    if (!err) {
        console.log('Connessione ottenuta');
        newsCol = db.collection(collectionName);
    }
    else{
        return console.dir(err);
    }
});



//console.log(optionsget.host+optionsget.path);


while(page < 80){
    console.log('page: '+page.toString());
    console.log('path: '+optionsget.host+optionsget.path+page.toString());
    //Call the new yoirk times REST API
    client.get(optionsget.host+optionsget.path+page.toString(), function(data, res){
        var news = JSON.parse(data);
        var docs = news.response.docs;

        //var newsCol = db.collection('News');

        if(newsCol != undefined){
            console.log('Inserting documents');
            for(var i = 0; i < docs.length; i++){
                delete docs[i]["_id"];
                newsCol.insert(docs[i], {w:1}, function(err, result) {
                    if(err){
                        return console.dir(err);
                    }
                });
            }
        }
        return console.log('Complete');
    }).on('error',function(err){
        console.log('something went wrong on the request', err.request.options);
    });
    page = page + 1;
}
