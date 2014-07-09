__author__ = 'andocavallari'
import json
from pymongo import MongoClient


file = '/Users/andocavallari/Downloads/topics2/TwitterPeek.json'
collectionName = 'News-TwitterPeek'

data = []
with open(file, 'r') as json_file:
    data = json.load(json_file)


client = MongoClient('localhost', 27017)
#Get a DB istance
db = client.BigData
#Get the collection
collection = db[collectionName]

for i in data:
    collection.insert(i)