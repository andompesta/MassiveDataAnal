import os
import json
from sys import argv
from gensim import corpora, models

from preprocess import Preprocessing

def readNewsFile(folder) :
	news = []
	paths = map(lambda x: folder+x, os.listdir(folder))
	i = 0
	for path in paths :
		os.system('clear')
		print "Parsing news: " + str(int((i/float(len(paths)))*100)) + '%'
		with open(path) as f :
			for j  in [json.loads(line.strip()) for line in f if line.strip() != ''] :
				news.append((j['_id'],j['topic'],j['full_text']))
		i += 1
	os.system('clear')
	print "Parsing news: " + str(int((i/float(len(paths)))*100)) + '%'
	return news


if __name__ == '__main__' :
	if len(argv) - 1 != 4 :
		print "USAGE: python tfidf.py newsFolder preprocessor outputFilename kTerms"
	else :
		newsFolder = argv[1]
		ppPath = argv[2]
		outputFilename = argv[3]
		kTerms = int(argv[4])

		news = readNewsFile(newsFolder)
		pp = Preprocessing.load(ppPath)

		texts = map(lambda x: pp.processDoc(x[-1]),news)

		dictionary = corpora.Dictionary(texts)
		corpus = [dictionary.doc2bow(text) for text in texts]
		tfidf = models.TfidfModel(corpus)

		output = []
		for (i,t,text) in news :
			tokens = pp.processDoc(text)
			bow = dictionary.doc2bow(tokens)
			summary = sorted(tfidf[bow],key=lambda x:x[1],reverse=True)[:kTerms]
			summary = map(lambda x:dictionary[x[0]],summary)

			output.append({'id':i,'topic':t,'summary':summary})

		with open(outputFilename,'w') as f :
			output = ''.join(map(lambda x: json.dumps(x)+'\n',output))
			f.write(output)



