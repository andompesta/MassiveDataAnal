import os
import json
from sys import argv
from gensim import corpora, models

from preprocess import Preprocessing

def readTweetsFiles(folder) :
	news = []
	paths = map(lambda x: folder+x, os.listdir(folder))
	i = 0
	
	for path in paths :
		os.system('clear')
		print "Parsing tweets: " + str(int((i/float(len(paths)))*100)) + '%'
		with open(path) as f :
			topic = path.partition('/')[-1].partition('-')[0]
			for contr in [json.loads(line.strip()) for line in f if line.strip() != ''] :
				contrTweets = []
				for t in contr :
					contrTweets.append(t['text'])

				text = ''.join(contrTweets)

				news.append((j['_id'],j['topic'],j['pub_date'],j['full_text']))
		i += 1
	
	os.system('clear')
	print "Parsing tweets: " + str(int((i/float(len(paths)))*100)) + '%'
	return news

def summarizeTweets(tweetsFolder,pp,outputFilename,kTerms) :
	news = readTweetsFiles(tweetsFolder)
	texts = map(lambda x: pp.processDoc(x[-1]),news)
	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]
	tfidf = models.TfidfModel(corpus)
	output = []

	for (i,t,d,text) in news :
		tokens = pp.processDoc(text)
		bow = dictionary.doc2bow(tokens)
		summary = sorted(tfidf[bow],key=lambda x:x[1],reverse=True)[:kTerms]
		summary = map(lambda x:dictionary[x[0]],summary)

		output.append({'id':i,'topic':t,'pub_date':d,'summary':summary})

	with open(outputFilename,'w') as f :
		output = ''.join(map(lambda x: json.dumps(x)+'\n',output))
		f.write(output)

if __name__ == '__main__' :

	if len(argv) - 1 != 4 :
		print "USAGE: python tweetsSummary.py tweetsFolder preprocessor outputFilename kTerms"
	else :
		tweetsFolder = argv[1]
		pp = Preprocessing.load(argv[2])
		outputFilename = argv[3]
		kTerms = int(argv[4])
		summarizeTweets(tweetsFolder,pp,outputFilename,kTerms)
