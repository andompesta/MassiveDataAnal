class TextComparator :
	def __init__(self, timeInterval, wordsValues) :
		self.timeInterval = timeInterval
		self.wordsValues = wordsValues
		self.bestText = ""
		self.bestScore = 0
		self.bestDate = None

	def compare(self, text) :
		if text["pub_date"] < self.timeInterval["begin"] or text["pub_date"] > self.timeInterval["end"] :
			return
		score = 0
		for word in text["content"].split() :
			word = word.lower()
			for wv in self.wordsValues :
				if wv["word"] == word :
					score += wv["value"]
		if score > self.bestScore :
			self.bestScore = score
			self.bestText = text["content"]
			self.bestDate = text["pub_date"]

	def printinfo(self) :
		print("\nNews published on: {0}\tScore:{1}\n{2}".format(self.bestDate, self.bestScore, self.bestText))
