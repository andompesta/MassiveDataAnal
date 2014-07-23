import json

def readNewsFile(path) :

	news = None
	
	with open(path) as f :
		topicJson = json.loads(f.read())
		news = {}
		for article in topicJson['articles'] :
			news[article['_id']['$oid']] = {'pub_date' : article['pub_date'], 'full_text' : article['full_text']}

	return news

def readShiftFile(shiftTweetsPath,shiftInfoPath) :

	shiftList = None
	with open(shiftInfoPath) as f :
		infoJson = json.loads(f.read())
		shiftList = infoJson['contradictions']

	with open(shiftTweetsPath) as f :
		topicContr = [json.loads(line.strip()) for line in f if line.strip() != '']

		for i in xrange(len(topicContr)) :
			shiftList[i]['tweets'] = [t['text'] for t in topicContr[i]]		
				
	return shiftList
