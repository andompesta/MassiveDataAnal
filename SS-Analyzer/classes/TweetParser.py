import json

class TweetParser :
	def __init__ (self, line) :
		self.content = []
		self.mintime = 0
		self.maxtime = 0
		tweets = json.loads(line)
		for t in tweets :
			self.content.append(t["text"])
			if self.mintime == 0 or t["time"] < self.mintime :
				self.mintime = t["time"]
			if self.maxtime < t["time"] :
				self.maxtime = t["time"]

	def getInterval(self) :
		return self.mintime, self.maxtime

	def getText(self) :
		return self.content

