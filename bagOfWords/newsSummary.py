import os
import json
from sys import argv
from gensim import corpora, models

from preprocess import Preprocessing

def readNewsFiles(folder) :
	news = []
	paths = map(lambda x: folder+x, os.listdir(folder))
	i = 0
	
	for path in paths :
		os.system('clear')
		print "Parsing news: " + str(int((i/float(len(paths)))*100)) + '%'
		with open(path) as f :
			topicJson = json.loads(f.read())
			for article in topicJson['articles'] :
				news.append((article['_id'],topicJson['topic'],article['pub_date'],article['full_text']))
		i += 1
	
	os.system('clear')
	print "Parsing news: " + str(int((i/float(len(paths)))*100)) + '%'
	return news

def summarizeNews(newsFolder,pp,outputFilename,kTerms) :
	news = readNewsFiles(newsFolder)
	texts = map(lambda x: pp.processDoc(x[-1]),news)
	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]
	tfidf = models.TfidfModel(corpus)
	output = []

	for (i,t,d,text) in news :
		tokens = pp.processDoc(text)
		bow = dictionary.doc2bow(tokens)
		summary = map(lambda x:(dictionary[x[0]],x[1]), sorted(tfidf[bow],key=lambda x:x[1],reverse=True)[:kTerms])

		output.append({'id':i,'topic':t,'pub_date':d,'summary':summary})

	with open(outputFilename,'w') as f :
		output = ''.join(map(lambda x: json.dumps(x)+'\n',output))
		f.write(output)

if __name__ == '__main__' :

	if len(argv) - 1 != 4 :
		print "USAGE: python newsSummary.py newsFolder preprocessor outputFilename kTerms"
	else :
		newsFolder = argv[1]
		pp = Preprocessing.load(argv[2])
		outputFilename = argv[3]
		kTerms = int(argv[4])
		summarizeNews(newsFolder,pp,outputFilename,kTerms)
