import os
import json

def readNewsFile(folder) :
	documents = []
	for path in map(lambda x: folder+x, os.listdir(folder)) :
		with open(path) as f :
			for j  in [json.loads(line) for line in f if line != ''] :
				documents.append(j['full_text'])
	return documents

def readTweetsFile(path) :
	documents = []
	for path in map(lambda x: folder+x, os.listdir(folder)) : 
		with open(path) as f :
			for j  in [json.loads(line) for line in f if line != ''] :
				for tweet in j :
					documents.append(tweet['text'])
	return documents


def



