import urllib2
import urllib
import json
from cookielib import CookieJar
#Crawler
from bs4 import BeautifulSoup
#Dbconnection
from pymongo import MongoClient
from sys import argv
import os

'''
TYPE OF MATERIAL TO BE IGNORED
- Summary: since it's a collection of short news from various topics
- Schedule: it's a list of events
- Op-Ed: "is a piece which expresses the opinions of a named author.". i guess this should be difficult to mine.
- Video: can be ignored. video description are rather short.
- Paid Death Notice: oh, come on!
- List: no meaningful data whatsoever



'''

# read all the json paths
json_paths = map(lambda f: argv[1]+f, os.listdir(argv[1]))

my_jsons = []
for path in json_paths :
	if 'system' not in path :
		with open(path) as f :
			j = []
			for line in f.read().strip().split('\n') :
				j.append(json.loads(line))
			
			my_jsons.append(j)

tom = {}

for topic in my_jsons :
	for article in topic :
		if article['type_of_material'] not in tom : 
			tom[article['type_of_material']] = 1
			print str(article['type_of_material']) + ': ' + article['web_url']
		else : tom[article['type_of_material']] += 1
'''

for topic in my_jsons :
	for article in topic :
		if article['type_of_material'] == 'News' : 
			print str(article['web_url'])
'''