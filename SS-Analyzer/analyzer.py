#!/usr/bin/python3

import argparse, configparser, time
from datetime import date
from classes.SpaceSaving import *
from classes.TweetParser import *
from classes.NewsParser import *
from classes.TextComparator import *

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
        
	# Parsing tweets and computing the more common words
	tweetsFileName = config["Paths"]["TweetsFile"].replace("X", args.topic)
	# commonWordsValues is a list of list of pair
	# it contains a list of pair <word, value> for each different contr. point
	commonWordsValues = []
	timeIntervals = []
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
			timeBegin, timeEnd = tweets.getInterval()
			dateBegin = date.fromtimestamp(timeBegin)
			dateEnd = date.fromtimestamp(timeEnd)
			timeIntervals.append({"begin":dateBegin, "end":dateEnd})
			print("Contradiction point {0} ranges between {1} and {2}".format(idx, dateBegin, dateEnd))
			print("Computing the list of more common words for contr. point {0}".format(idx))
			idx += 1
			tweetsText = tweets.getText()
			for t in tweetsText :
				for word in t.split() :
					ss.notify(word)
			commonWordsValues.append(ss.getSmartList())

	# Comparing with news
	np = NewsParser(config["Paths"]["NewsFile"].replace("X", args.topic))
	news = np.getNewsText()
	comparator = []
	for idx, i in enumerate(timeIntervals) :
		comparator.append(TextComparator(i, commonWordsValues[idx]))
	for n in news :
		for idx, i in enumerate(timeIntervals) :
			comparator[idx].compare(n)

	for c in comparator :
		c.printinfo()

