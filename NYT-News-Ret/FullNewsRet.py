__author__ = 'andocavallari'
import urllib2
import urllib
import json
from cookielib import CookieJar
#Crawler
from bs4 import BeautifulSoup
#Dbconnection
from pymongo import MongoClient



collectionName = 'News-Hangover'
userid = 'ando.cavallari@hotmail.it'
password = 'vela1990'

client = MongoClient()
client = MongoClient('localhost', 27017)
#Get a DB istance
db = client.BigData
#Get the collection
collection = db[collectionName]

#Enable cookies
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'userid' : userid, 'password' : password})
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.open('https://myaccount.nytimes.com/auth/login', login_data)



for metaNew in collection.find():
    htmlUrl = metaNew["web_url"]
    print(htmlUrl)
    htmlPage = opener.open(htmlUrl)
    soup = BeautifulSoup(htmlPage.read())
    text = " "


    #check numbero of page
    if soup.find("a", class_ = "next") != None:
        print("2 pagine nel documento")
    else:

        # for aBody in soup.find_all("div", class_ = "articleBody"):
        #     for paragraf in aBody.find_all("p"):
        #         for string in paragraf.stripped_strings:
        #             text = text + string
        for textPart in soup.find_all("p", class_ = "story-body-text"):
            for string in textPart.stripped_strings:
                text = text + string

    if(text != " "):
        metaNew['full_text'] = text
        collection.update({'_id':metaNew['_id']},metaNew , upsert=False, multi=False)
db.close




    #
    # for aBody in soup.find_all("div", class_ = "articleBody"):
    #     for paragraf in aBody.find_all("p"):
    #         for string in paragraf.stripped_strings:
    #             text = text + string


    # for textPart in soup.find_all("p", itemprop = "articleBody"):
    #     for string in textPart.stripped_strings:
    #         text = text + string


