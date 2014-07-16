import json

class TweetParser :
	def __init__ (self, line) :
		tweets = json.loads(line)
		self.content = [t["text"] for t in tweets]
	
	def getText(self) :
		return self.content
