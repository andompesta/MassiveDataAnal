#!/usr/bin/python3

import argparse, configparser, time
from datetime import date
from classes.SpaceSaving import *
from classes.TweetParser import *
from classes.NewsParser import *
from classes.TextComparator import *
from classes.WikiParser import *

if __name__ == "__main__" :
	# Parsing arguments...
	parser = argparse.ArgumentParser(description="Finds the more similar news")
	parser.add_argument("-t", help="Topic to analyze", required=True, dest="topic")
	args = parser.parse_args()
	# ... and the configuration file
	config = configparser.RawConfigParser()
	config.read("config.ini")
	# Reading the stop words file
	swf = config["Paths"]["StopWordFile"]
	try :
		with open(swf, "r") as fin :
			stopWords = [line.rstrip("\n") for line in fin]
	except IOError :
		print("WARNING: no stopwords file or invalid file")
	
	# Getting contradiction time interval
	contrFile = open(config["Paths"]["ContrInfo"].replace("X", args.topic), "r")
	contrIntervals = json.load(contrFile)
	timeIntervals = list(map(lambda x: {"begin":date.fromtimestamp(x["timeBegin"]), "end":date.fromtimestamp(x["timeEnd"])}, \
						contrIntervals["contradictions"]))
	print("{0} contradictions points in the selected topic".format(len(timeIntervals)))
	for ti in timeIntervals : print("{0} - {1}".format(ti["begin"], ti["end"]))
	
	# Parsing tweets and computing the more common words
	tweetsFileName = config["Paths"]["ContrTweets"].replace("X", args.topic)
	# commonWordsValues is a list of list of pair
	# it contains a list of pair <word, value> for each different contr. point
	commonWordsValues = []
	with open(tweetsFileName, "r") as tfile :
		idx = 1
		# Each line corresponds to a different contradiction point
		# We have to parse each line independently from the others
		# and compute the list of more common words for each of them.
		# Also, while parsing them, we also compute the time interval
		# the tweets have been published in
		for line in tfile :
			ss = SpaceSaving(size=100, stopWordsList=(stopWords or []))
			tweets = TweetParser(line)
			print("Computing the list of more common words for contr. point {0}".format(idx))
			idx += 1
			tweetsText = tweets.getText()
			for t in tweetsText :
				for word in t.lower().split() :
					ss.notify(word)
			commonWordsValues.append(ss.getSmartList())

	# Initializing the comparator class
	wsize = date.timedelta(days=3)
	comparator = [TextComparator(i, wsize, commonWordsValues[idx]) for idx, i in enumerate(timeIntervals)]
	# Reading news from NYT and comparing
	print("Reading news from NYT")
	np = NewsParser("NYT", config["Paths"]["NYTFile"].replace("X", args.topic), args.topic)
	news = np.getNewsText()
	for n in news :
		for idx in range(len(timeIntervals)) :
			comparator[idx].compare(n, "NYT")
	# Reading news from ABC Australia
	print("Reading news from ABC")
	np = NewsParser("ABC", config["Paths"]["ABCfile"].replace("X", args.topic), args.topic)
	news = np.getNewsText()
	for n in news :
		for idx in range(len(timeIntervals)) :
			comparator[idx].compare(n, "ABC Australia")
	# Reading news from wikipedia and comparing
	print("Reading news from Wikipedia")
	wp = WikiParser(config["Paths"]["WikiEvents"], config["Paths"]["WikiDeaths"])
	wikis = wp.getNewsText()
	for n in wikis :
		for idx in range(len(timeIntervals)) :
			comparator[idx].compare(n, "Wikipedia")
	# Printing results
	for c in comparator :
		c.printinfo()

