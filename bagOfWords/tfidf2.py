from gensim import corpora, models
import json,os

from parsing import readNewsFile,readShiftFile
from utilities import readConfigFile,unixTime
from preprocess import Preprocessing


def TF_IDF(shifts,tweets,news,topK,topS,preprocessor) :

	# creates the dictionary and the model on the whole twitter corpus
	dictionary = corpora.Dictionary()
	corpus = []
	for t in tweets :
		corpus.append(dictionary.doc2bow(preprocessor.processDoc(t['text']),allow_update = True))
	
	tfidf = models.TfidfModel(corpus)

	summaries = []

	for shift in shifts :

		# computes the top-k-keywords by summing the TF-IDF values for each token in the shift tweets
		keywords = {}
		for tweet in shift['tweets'] :
			tokens = preprocessor.processDoc(tweet)
			bow = dictionary.doc2bow(tokens)
			for key,value in tfidf[bow] :
				if dictionary[key] in keywords : keywords[dictionary[key]] += value
				else : keywords[dictionary[key]] = value

		keywords = dict(sorted(keywords.items(),key=lambda x:x[1],reverse=True)[:topK])

		# selects the news falling into the shift window and splits them in sentences, ranking them according to the keywords TF-IDF values
		tBegin = shift['timeBegin']
		tEnd = shift['timeEnd']
		span = 3600*24*5
		candidateNews = [news[artId]['full_text'] for artId in news if 'full_text' in news[artId] and unixTime(news[artId]['pub_date']) <= tEnd + span and unixTime(news[artId]['pub_date']) >= tBegin - span]
		sentences = {}
		for s in [s for n in candidateNews for s in n.split('\n')] :
			score = 0
			for token in s.split(' ') :
				if token in keywords : score += keywords[token]
			sentences[s] = score / len(s.split(' '))

		total_score = 0
		text = ''
		for s,score in sorted(sentences.items(),key=lambda x:x[1],reverse=True)[:topS] :
			text = text + '\n' + s
			total_score += score
		summaries.append( {'summary':text.strip(),'score':total_score,'keywords':sorted(keywords.items(),key=lambda x:x[1],reverse=True)} )

	return summaries

if __name__ == '__main__' :
	from sys import argv
	if len(argv) -1 != 8 :
		print '''[ERR] Parameters:
		-tweets file
		-news file
		-shift info file
		-shift tweets file
		-top-k-keywords
		-top-s-sentences
		-config file
		-output file'''
		exit()
	else :
		with open(argv[1]) as f :
			tweets = json.loads(f.read())
		news = readNewsFile(argv[2])
		shifts = readShiftFile(argv[4],argv[3])		
		topK,topS = int(argv[5]),int(argv[6])

		params = readConfigFile(argv[7])
		with open(params['punctuation_file']) as f :
			punctuation = f.read().strip().replace('\n',' ').split()
		with open(params['stopwords_file']) as f :
			stopwords = f.read().strip().replace('\n',' ').split()
		with open(params['dpatterns_file']) as f :
			dpatterns = f.read().strip().replace('\n',' ').split()
		threshold = int(params['threshold'])
		preprocessor = Preprocessing(punctuation=punctuation,stopwords=stopwords,dpatterns=dpatterns,threshold=threshold,removeURLs=True,removeUnicode=True)

		with open(argv[8],'w') as f :
			f.write(json.dumps(TF_IDF(shifts,tweets,news,topK,topS,preprocessor)))

