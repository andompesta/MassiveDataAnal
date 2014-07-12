#!/usr/bin/python3

import configparser, argparse, random, json, subprocess
from datetime import date, timedelta
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

	# Loading stopwords
	fin = open(config["Paths"]["StopWordsFile"], 'r')
	stopWords = list(map(lambda x: x.strip().lower(), fin.readlines()))

	# Loading tweets
	fin = open(tweetsFile, 'r')
	contrTweetList = [json.loads(line) for line in fin]
	
	# Loading news
	NYTNews = NewsParser(NYTFile, args.topic)
	ABCNews = NewsParser(ABCFile, args.topic)
	allNews = NYTNews.getNewsText() + ABCNews.getNewsText()
	windowSize = timedelta(days=3)
	contrNews = [[news for news in allNews if news["pub_date"] > (inter["begin"]-windowSize) and news["pub_date"] < (inter["end"]+windowSize)] for inter in intervals]
	
	# Iterating and computing score
	
	commit = subprocess.check_output(["git", "show", "--oneline"])
	print(str(commit))
	ss = 0
	gram = 0
	lsa = 0
	for i in range(len(contrList)) :
		print("\nAnalyzing performances for contradiction point {0}/{1} ({2} news in the interval)".format(i+1, len(contrList), len(contrNews[i])))
		if len(contrNews[i]) < 2 :
			print("Skipping this contradiction point, since there are not enough news")
			continue
		# Comparing with tweets
		print("From 0 to 10 then how much do you think the summaries represent the following 5 tweets?")
		sampleList = random.sample(contrTweetList[i], 5)
		for t in sampleList : print(t["text"])
		ss, gram, lsa = getScore(4, ss, gram, lsa)
		# Against random samples from news
		nsamples = min(5, len(contrNews[i]))
		print("I'm going to take {0} random news in the contradiction interval and taking 10 random words from each of them".format(nsamples))
		print("Please say how many of this randomly generated summaries outcome the results")
		newsSample = random.sample(contrNews[i], nsamples)
		newsSampleWords = [news["content"].lower().split() for news in newsSample]
		for n in newsSampleWords : n = filter(lambda x: x not in stopWords, n)
		wordSample = [random.sample(news, 10) for news in newsSampleWords]
		for w in wordSample : print(w)
		ss, gram, lsa = getScore(-3, ss, gram, lsa)
		print("Now do as in the previous test, but with respect to the following headlines")
		newsSample = random.sample(contrNews[i], nsamples)
		for news in newsSample : print(news["content"][0:100])
		ss, gram, lsa = getScore(-1, ss, gram, lsa)
	
	print("\n" + str(commit))
	print("Scores: SS={0}\tngram={1}\tLSA={2}".format(ss, gram, lsa))
