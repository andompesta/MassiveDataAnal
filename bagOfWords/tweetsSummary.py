import os
import json
from sys import argv
from gensim import corpora, models

from preprocess import Preprocessing

def readTweetsFiles(tweetsFolder,infoFolder) :
	
	# reads the contradiction info files
	contradictionList = {}
	infoPaths = map(lambda x: infoFolder+x, os.listdir(infoFolder))
	for path in infoPaths :
		topic = path.split('/')[-1].partition('.')[0]
		contradictionList[topic] = {'topic' : topic}

		with open(path,'r') as f :
			infoJson = json.loads(f.read())
			contradictionList[topic]['contradictions'] = infoJson['contradictions']

	# reads the contradiction tweets files
	tweetsPaths = map(lambda x: tweetsFolder+x, os.listdir(tweetsFolder))
	i = 0
	for path in tweetsPaths :
		os.system('clear')
		print "Parsing tweets: " + str(int((i/float(len(tweetsPaths)))*100)) + '%'
		with open(path) as f :
			topic = path.split('/')[-1].partition('-')[0]
			topicContr = [json.loads(line.strip()) for line in f if line.strip() != '']
			
			for j in xrange(len(topicContr)) :
				contrText = []

				for t in topicContr[j] :
					contrText.append(' '+t['text'])

				text = ''.join(contrText).strip()
				contradictionList[topic]['contradictions'][j]['text'] = text

		i += 1
	
	os.system('clear')
	print 'Parsing tweets: ' + str(int((i/float(len(tweetsPaths)))*100)) + '%'
	return contradictionList.values()

def summarizeTweets(tweetsFolder,infoFolder,pp,outputFilename,kTerms) :
	contradictionList = readTweetsFiles(tweetsFolder,infoFolder)

	print 'Generating the model'
	texts = []
	for topic in contradictionList :
		for contr in topic['contradictions'] :
			texts.append( pp.processDoc(contr['text']) )

	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]
	tfidf = models.TfidfModel(corpus)

	print 'Computing the summaries'
	for topic in contradictionList :
		for contr in topic['contradictions'] :

			tokens = pp.processDoc(contr['text'])
			bow = dictionary.doc2bow(tokens)
			contr['summary'] = map(lambda x:(dictionary[x[0]],x[1]), sorted(tfidf[bow],key=lambda x:x[1],reverse=True)[:kTerms])
			contr.pop('text')

	with open(outputFilename,'w') as f :
		f.write(json.dumps(contradictionList))

if __name__ == '__main__' :

	if len(argv) - 1 != 5 :
		print "USAGE: python tweetsSummary.py tweetsFolder infoFolder preprocessor outputFilename kTerms"
	else :
		tweetsFolder = argv[1]
		infoFolder = argv[2]
		pp = Preprocessing.load(argv[3])
		outputFilename = argv[4]
		kTerms = int(argv[5])
		summarizeTweets(tweetsFolder,infoFolder,pp,outputFilename,kTerms)
