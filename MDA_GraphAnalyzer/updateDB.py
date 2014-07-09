__author__ = 'andocavallari'
import urllib2
import json
#Dbconnection
from pymongo import MongoClient
collectionName = 'News-Cern'
#Get the DB client connection
client = MongoClient()
client = MongoClient('localhost', 27017)
#Get a DB istance
db = client['MDA_News']
#Get the collection
collection = db[collectionName]


for i in collection.find():
    text = i["full_text"]
    print(text)
    text = text.replace(". ", ".\n")
    print(text)
    i["full_text"] = text
    collection.save(i)