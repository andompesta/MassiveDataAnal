from gensim import corpora, models, similarities
import json,os

from parsing import readNewsFile,readShiftFile
from utilities import readConfigFile,unixTime
from preprocess import Preprocessing


def LSI(shifts,tweets,news,lsiDimensions,topS,preprocessor) :

	# creates the dictionary and trains the LSI model on the whole twitter corpus
	dictionary = corpora.Dictionary()
	corpus = []
	for t in tweets :
		corpus.append(dictionary.doc2bow(preprocessor.processDoc(t['text']),allow_update = True))
	
	print "Generating the model"
	lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=lsiDimensions)

	summaries = []

	for shift in shifts :

		# creates an index with each tweet belonging to the shift
		print "Generating an index"
		index = similarities.MatrixSimilarity(lsi[[dictionary.doc2bow(t.split()) for t in shift['tweets']]])
		
		# selects the news falling into the shift window and splits them in sentences
		tBegin = shift['timeBegin']
		tEnd = shift['timeEnd']
		span = 3600*24*5
		candidateNews = [news[artId]['full_text'] for artId in news if 'full_text' in news[artId] and unixTime(news[artId]['pub_date']) <= tEnd + span and unixTime(news[artId]['pub_date']) >= tBegin - span]
		sentences = [s for n in candidateNews for s in n.split('\n')]

		print "Computing similarities"
		simList = enumerate([sum(map(lambda x:x[1],index[lsi[[dictionary.doc2bow(s.split())]]])) for s in sentences])
		
		# takes the s most similar sentences according to the previously genenerated index
		total_similarity = 0.0
		text = ''
		for i,similarity in sorted(simList, key=lambda x: -x[1])[:topS] :
			text = text + '\n' + sentences[i]
			total_similarity += similarity
		total_similarity = total_similarity / topS
		summaries.append( {'summary':text.strip(),'similarity':total_similarity} )

	return summaries

if __name__ == '__main__' :
	from sys import argv
	if len(argv) -1 != 8 :
		print '''[ERR] Parameters:
		-tweets file
		-news file
		-shift info file
		-shift tweets file
		-number of LSI dimensions
		-top-s-sentences
		-config file
		-output file'''
		exit()
	else :
		with open(argv[1]) as f :
			tweets = json.loads(f.read())
		news = readNewsFile(argv[2])
		shifts = readShiftFile(argv[4],argv[3])		
		lsiDimensions,topS = int(argv[5]),int(argv[6])

		params = readConfigFile(argv[7])
		with open(params['punctuation_file']) as f :
			punctuation = f.read().strip().replace('\n',' ').split()
		with open(params['stopwords_file']) as f :
			stopwords = f.read().strip().replace('\n',' ').split()
		with open(params['dpatterns_file']) as f :
			dpatterns = f.read().strip().replace('\n',' ').split()
		threshold = int(params['threshold'])
		preprocessor = Preprocessing(punctuation=punctuation,stopwords=stopwords,dpatterns=dpatterns,threshold=1,removeURLs=True,removeUnicode=True)

		with open(argv[8],'w') as f :
			f.write(json.dumps(LSI(shifts,tweets,news,lsiDimensions,topS,preprocessor)))

