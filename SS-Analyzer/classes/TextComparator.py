try :
	import statistics
except ImportError :
	print("WARNING: python 3.4 is required to compute the statistics")
	print("If you don't care about stats you can go ahead, everything will be fine")

class TextComparator :
	def __init__(self, timeInterval, wordsValues) :
		self.timeInterval = timeInterval
		self.wordsValues = wordsValues
		self.scoreList = []
		self.bestText = ""
		self.bestScore = 0
		self.bestDate = None
		self.bestPublisher = None

	def compare(self, text, publisher) :
		if text["pub_date"] < self.timeInterval["begin"] or text["pub_date"] > self.timeInterval["end"] :
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

	def printinfo(self) :
		if len(self.scoreList) == 0 :
			print("\nNo news found in the selected time period")
			return
		print("\nAnalyzed {0} news".format(len(self.scoreList)))
		try :
			mean = statistics.mean(self.scoreList)
			stdev = statistics.stdev(self.scoreList)
		except statistics.StatisticsError :
			print("WARNING: not enough point to compute mean and standard deviation")
			mean = stdev = 0
		except ImportError :
			print("WARNING: python 3.4 is required to compute the statistics")
			mean = stdev = 0
		print("Mean: {0}\nStdDev: {1}".format(mean, stdev))
		print("Best news published on: {0} by {3}\tScore:{1}\n{2}...".format(self.bestDate, self.bestScore, self.bestText, self.bestPublisher))
