import string
try :
	import statistics
	EnableStats = True
except ImportError :
	EnableStats = False
	print("\033[93mWARNING: python 3.4 is required to compute the statistics\033[0m")
	print("If you don't care about stats you can go ahead, everything will be fine\n")
try :
	import nltk, nltk.data
	forceSplitsAtParagraph = False
except ImportError :
	forceSplitsAtParagraph = True
	print("\033[93mWARNING: nltk or nltk-data are required to split at sentence level\033[0m")
	print("Split will be forced at paragraph level\n")

class bestStorer :
	def __init__(self, n) :
		self.resultList = []
		self.size = n
	
	def test(self, element, score) :
		if len(self.resultList) < self.size : 
			self.resultList.append({"sentence":element, "score":score})
			self.resultList.sort(key=(lambda x: x["score"]), reverse=True)
		elif score > self.resultList[-1]["score"] :
			self.resultList[-1] = {"sentence":element, "score":score}
			self.resultList.sort(key=(lambda x: x["score"]), reverse=True)

	def print(self) :
		for s in self.resultList : print("{0} ({1})".format(s["sentence"],s["score"]))




class TextComparator :
	def __init__(self, timeInterval, windowsize, wordsValues) :
		self.timeInterval = timeInterval
		self.windowsize = windowsize
		self.wordsValues = wordsValues
		self.scoreList = []
		self.IntervalNews = 0
		self.bestText = ""
		self.bestScore = 0
		self.bestDate = None
		self.bestPublisher = None
		self.bestSentences = bestStorer(1)

	def compareNews(self, text, publisher) :
		if text["pub_date"] < (self.timeInterval["begin"] - self.windowsize) or text["pub_date"] > (self.timeInterval["end"] +self.windowsize) :
			return
		score = 0
		for word in text["content"].lower().split() :
			for wv in self.wordsValues :
				if wv["word"] == word :
					score += wv["value"]
		self.scoreList.append(score)
		if score > self.bestScore :
			self.bestScore = score
			self.bestText = text["content"][:150]
			self.bestDate = text["pub_date"]
			self.bestPublisher = publisher

	def compareSentences(self, text, splitsAtSentence) :
		if text["pub_date"] < (self.timeInterval["begin"] - self.windowsize) or text["pub_date"] > (self.timeInterval["end"] +self.windowsize) :
			return
		self.IntervalNews += 1
		if splitsAtSentence :
			tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
			sentences = tokenizer.tokenize(text["content"])
		else :	
			sentences = text["content"].split('\n')

		punct = set(string.punctuation)
		for s in sentences :
			score = 0
			wordsList = s.lower().split()
			for w in wordsList :
				wCleaned = ''.join(ch for ch in w if ch not in punct)
				for wv in self.wordsValues :
					if wv["word"] == wCleaned : score += wv["value"]
			score /= len(wordsList)
			self.bestSentences.test(s, score)

	def printinfo(self) :
		if len(self.scoreList) == 0 :
			print("\nNo news found in the selected time period")
			return
		print("\nAnalyzed {0} news".format(len(self.scoreList)))
		if EnableStats :
			try :
				mean = statistics.mean(self.scoreList)
				stdev = statistics.stdev(self.scoreList)
			except statistics.StatisticsError :
				print("WARNING: not enough point to compute mean and standard deviation")
				mean = stdev = 0
			print("Mean: {0}\nStdDev: {1}".format(mean, stdev))
		print("Best news published on: {0} by {3}\tScore:{1}\n{2}...".format(self.bestDate, self.bestScore, self.bestText, self.bestPublisher))

	def printSentences(self) :
		print("\nAnalyzed {0} news".format(self.IntervalNews))
		self.bestSentences.print()
