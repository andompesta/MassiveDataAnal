#!/usr/bin/python3

import requests, argparse, sys, json
from bs4 import BeautifulSoup

months = { "January":1, \
		"February":2, \
		"March":3, \
		"April":4, \
		"May":5, \
		"June":6, \
		"July":7, \
		"August":8, \
		"September":9, \
		"October":10, \
		"November":11, \
		"December":12, \
		}


def newsParser(errf, url, newsID) :
	try :
		response = requests.get(url)
		soup = BeautifulSoup(response.text)
		article = soup.find("div", attrs={"class":"article section"})
		if article == None :
			raise Exception("No article section")
		h1 = article.find("h1")
		title = h1.get_text()
		pub_date = article.find("p", attrs={"class":"published"}).find("span", attrs={"class":"timestamp"}).get_text()
		pub_date = pub_date.lstrip().rstrip()
		dateToken = pub_date.split()
		fpub_date = "{0}-{1}-{2}T{3}Z".format(dateToken[2], months[dateToken[0]], dateToken[1].rstrip(','), dateToken[3])
		full_text = ""
		lead_paragraph = ""
		for p in article.find_all("p") :
			if p.has_attr("class") :
				continue
			elif lead_paragraph == "" :
				lead_paragraph = p.get_text()
			else :
				full_text += p.get_text()
		return {"title":title, "lead_paragraph":lead_paragraph, "full_text":full_text, "pub_date":fpub_date, "_id":{"$oid":newsID}}
	except Exception as exc :
		print("ERROR: Unreadable schema detected. Details can be found on log file")
		errf.write(str(exc) + '\n')
		errf.write(url + '\n')
		raise exc


if __name__ == "__main__" :
	parser = argparse.ArgumentParser(description="Get news about a given topic from Australian ABC")
	parser.add_argument("-t", help="The keyword to search for", required=True, dest="topic")
	args = parser.parse_args()
	# Downloading the main page
	newsURLs = []
	GETparams = { "tab":"advanced", \
		"query": args.topic, \
		"query_and":"", \
		"query_phrase":"", \
		"query_or":"", \
		"query_not":"", \
		"sort":"Relevance", \
		"meta_f_sand":"", \
		"meta_a":"", \
		"meta_s":"", \
		"meta_t":"", \
		"meta_d1day":"1", \
		"meta_d1month":"Jan", \
		"meta_d1year":"2009", \
		"meta_d2day":"31", \
		"meta_d2month":"Dec", \
		"meta_d2year":"2009"}
	response = requests.get("http://www.abc.net.au/news/search/?", params=GETparams)
	#print("Got the list of available news from " + response.url)
	soup = BeautifulSoup(response.text)
	HTMLnewsList = soup.find("ul", attrs={"class":"article-index"})
	if HTMLnewsList == None :
		print("It seems no news list is present in that page")
		sys.exit()
	acceptableClassType = ["media"]
	knownClassType = ["image", "Video", "Audio"]
	for title in HTMLnewsList.find_all("h3") :
		classType = title.find("span", attrs={"class":"type"})
		if (classType == None or classType.string in acceptableClassType) :
			link = title.find('a')
			newsURLs.append(link.get('href'))
		elif (classType.string not in knownClassType) :
			print("WARNING: new class type {0} has been detected".format(classType.string))

	print("{0} news have been selected for download".format(len(newsURLs)))
	# Downloading the news
	trimmedTopic = args.topic.replace(" ", "")
	idBase = "ABC" + trimmedTopic
	with open("abc_{0}.json".format(trimmedTopic), "w") as outf :
		with open("errors.log", "w") as errf :
			articles = []
			for idx, url in enumerate(newsURLs) :
				print("Downloading and parsing news {0}/{1}".format(idx+1, len(newsURLs)))
				articles.append(newsParser(errf, "http://www.abc.net.au" + url, idBase+str(idx)))
			outf.write(json.dumps({"topic" : trimmedTopic, "articles" : articles}))
