#!/usr/bin/python3

import requests, argparse, sys, json
from bs4 import BeautifulSoup

def newsParser(outf, errf, url) :
	try :
		response = requests.get(url)
		soup = BeautifulSoup(response.text)
		article = soup.find("div", attrs={"class":"article section"})
		if article == None :
			raise Exception("No article section")
		h1 = article.find("h1")
		title = h1.get_text()
		pub_date = article.find("p", attrs={"class":"published"}).find("span", attrs={"class":"timestamp"}).string
		full_text = ""
		for idx, p in enumerate(article.find_all("p")) :
			if idx == 0 :
				lead_paragraph = p.get_text()
		#	elif p["class"] == "topics" :
		#		break
			else :
#				for attr,val in p.attrs :
#					if val == "topics" :
#						break
				full_text += p.get_text()
		newsJSON = json.dumps({"title":title, "lead_paragraph":lead_paragraph, "full_text":full_text, "pub_date":pub_date})
		outf.write(newsJSON + '\n')
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
	with open("abc_{0}.json".format(args.topic), "w") as outf :
		with open("errors.log", "w") as errf :
			for idx, url in enumerate(newsURLs) :
				print("Downloading and parsing news {0}/{1}".format(idx+1, len(newsURLs)))
				newsParser(outf, errf, "http://www.abc.net.au" + url)
