__author__ = 'andocavallari'
import urllib2
import json
from pymongo import MongoClient


accountKey = "54f0ec76fac6c0a6b95df02b38c6216a:16:69289018"
page = 0
endPage = 27
collectionName = 'News-SuperBowl'
query = 'Super%20Bowl'
startingDate = '20091002'
endDate = '20091231'

urlOption = {
    'host' : "http://api.nytimes.com/svc/search/",
    'path' : "v2/articlesearch.json?q="+query+"&sort=oldest&begin_date="+startingDate+"&end_date="+endDate+"&api-key="+str(accountKey)+"&page="
    #'path' : "v2/articlesearch.json?q="+query+"&sort=oldest&begin_date=20090101&end_date=20091201&api-key="+str(accountKey)+"&page="
}

#Get the DB client connection
client = MongoClient()
client = MongoClient('localhost', 27017)
#Get a DB istance
db = client.BigData
#Get the collection
collection = db[collectionName]


while(page <= endPage):
    #Make a RESTful API request
    print(urlOption['host']+urlOption['path']+str(page))
    req = urllib2.urlopen(urlOption['host']+urlOption['path']+str(page))

    #Get the json data
    data = json.load(req)
    news = data["response"]["docs"]

    #Delete the id fild
    for i in news:
        del i['_id']
        #insert the news in the DB
        collection.insert(i)
    page = page + 1



#print(data)