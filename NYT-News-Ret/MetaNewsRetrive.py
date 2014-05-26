__author__ = 'andocavallari'
import urllib2
import json
from cookielib import CookieJar
#Crawler
from bs4 import BeautifulSoup
#Dbconnection
from pymongo import MongoClient


accountKey = "0022795243a8f95c00655155d3701261:7:69418463"
page = 0
endPage = 10
collectionName = 'FullNewsTry'
query = 'Obama'
startingDate = '20140508'
endDate = '20140509'

urlOption = {
    'host' : "http://api.nytimes.com/svc/search/",
    'path' : "v2/articlesearch.json?q="+query+"&sort=oldest&begin_date="+startingDate+"&end_date="+endDate+"&api-key="+str(accountKey)+"&page="
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

#Enable cookies
    cj = CookieJar()
    for i in news:
        htmlUrl = i["web_url"]
        print(htmlUrl)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        htmlPage = opener.open(htmlUrl)
        soup = BeautifulSoup(htmlPage.read())
        text = ""
        for textPart in soup.find_all("p", class_ = "story-body-text story-content"):
            for string in textPart.stripped_strings:
                text = text + string
        print (text)
        obj = {
            'title' : i["headline"],
            'date' : i["pub_date"],
            'text' : text
        }
        collection.insert(obj)
    page = page + 1

#print(data)
