#!/usr/bin/python3

import configparser, argparse, random, json
from datetime import date
from classes.NewsParser import NewsParser


def getScore(factor, ss, ngram, lsa) :
	ss += int(input("\tValue for SS Analyzer: ")) * factor
	ngram += int(input("\tValue for nGram Analyzer: ")) * factor
	lsa += int(input("\tValue for LSA Analyzer: ")) * factor
	return ss, ngram, lsa


if __name__ == "__main__" :
	parser = argparse.ArgumentParser("Helps scoring different techniques")
	parser.add_argument("-t", dest="topic", required=True, help="the topic")
	args = parser.parse_args()
	config = configparser.ConfigParser()
	config.read("config.ini")
	
	contrFile = config["Paths"]["ContrFile"].replace("XXX", args.topic)
	tweetsFile = config["Paths"]["TweetFile"].replace("XXX", args.topic)
	NYTFile = config["Paths"]["NYTNewsFile"].replace("XXX", args.topic)
	ABCFile = config["Paths"]["ABCNewsFile"].replace("XXX", args.topic)
	
	# Loading contradiction file
	fin = open(contrFile, 'r')
	contrList = json.load(fin)["contradictions"]
	intervals = list(map(lambda x: {"begin":date.fromtimestamp(x["timeBegin"]), "end":date.fromtimestamp(x["timeEnd"])}, contrList))

	# Loading tweets
	fin = open(tweetsFile, 'r')
	contrTweetList = [json.loads(line) for line in fin]
	
	# Loading news
	NYTNews = NewsParser(NYTFile, args.topic)
	ABCNews = NewsParser(ABCFile, args.topic)
	allNews = NYTNews.getNewsText() + ABCNews.getNewsText()
	contrNews = [[news for news in allNews if news["pub_date"] > inter["begin"] and news["pub_date"] < inter["end"]] for inter in intervals]
	
	# Iterating and computing score
	ss = 0
	gram = 0
	lsa = 0
	for i in range(len(contrList)) :
		print("\nAnalyzing performances for contradiction point {0}/{1}".format(i+1, len(contrList)))
		# Comparing with tweets
		print("From 0 to 10 then how much do you think the summaries represent the following 5 tweets?")
		sampleList = random.sample(contrTweetList[i], 5)
		for t in sampleList : print(t["text"])
		ss, gram, lsa = getScore(4, ss, gram, lsa)
		# Against random samples from news
		nsamples = min(5, len(contrNews[i]))
		print("I'm going to take {0} random news in the contradiction interval and taking 10 random words from each of them".format(nsamples))
		print("Please say how many news each summary outcomes (i.e. if you think the given summary is better than two of the following, but worse than the other 3, write 2)")
		newsSample = random.sample(contrNews[i], nsamples)
		wordSample = [random.sample(news["content"].split(), 10) for news in newsSample]
		for w in wordSample : print(w)
		ss, gram, lsa = getScore(2, ss, gram, lsa)
		print("Now do as in the previous test, but with respect to the following headlines")
		newsSample = random.sample(contrNews[i], nsamples)
		for news in newsSample : print(news["content"][0:50])
		ss, gram, lsa = getScore(1, ss, gram, lsa)

	print("Scores: SS={0}\tngram={1}\tLSA={2}".format(ss, gram, lsa))
