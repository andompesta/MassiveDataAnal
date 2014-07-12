import os
import json
from gensim import corpora, models

from preprocess import Preprocessing
from utilities import readConfigFile

def readNewsFile(path) :

	news = None
	
	with open(path) as f :
		topicJson = json.loads(f.read())
		topic = topicJson['topic']
		news = {}
		for article in topicJson['articles'] :
			news[article['_id']['$oid']] = {'pub_date' : article['pub_date'], 'full_text' : article['full_text']}

	return topic,news

def summarizeNews(newsFolder,pp,outputFolder,kTerms) :
	
	paths = map(lambda x: newsFolder+x, os.listdir(newsFolder))

	for path in paths :

		topic,news = readNewsFile(path)
		
		baseline = []

		for article in news.values() :
			baseline.append(pp.processDoc(article['full_text']))

		dictionary = corpora.Dictionary(baseline)
		corpus = [dictionary.doc2bow(text) for text in baseline]
		tfidf = models.TfidfModel(corpus)
		
		for artId in news :
			tokens = pp.processDoc(news[artId]['full_text'])
			bow = dictionary.doc2bow(tokens)
			summary = map(lambda x:(dictionary[x[0]],x[1]), sorted(tfidf[bow],key=lambda x:x[1],reverse=True)[:kTerms])
			news[artId]['summary'] = summary
			news[artId].pop('full_text')

		with open(outputFolder + topic + '.json','w') as f :
			f.write(json.dumps(news))

if __name__ == '__main__' :
	import getopt
	import sys

	usage = '''PARAMS:
	-c\tConfiguration file path
	-o\tOutput folder
	-k\tSummary size

	-s\tPath of the stopwords file (OPTIONAL)
	-p\tPath of the punctuation file (OPTIONAL)
	-d\tPath of the discard-pattern file (OPTIONAL)
	-t\tThreshold (OPTIONAL)
	'''

	try :
		opts, args = getopt.getopt(sys.argv[1:], "c:o:k:s:p:d:t:")
	except getopt.GetoptError as err :
		sys.stderr.write(str(err) + '\n')
		print usage
		sys.exit(2)

	configurationPath = None
	outputFolder = None
	summarySize = None

	stopwordsFile = None
	punctuationFile = None
	dpatternsFile = None

	stopwords = set()
	punctuation = set()
	dpatterns = set()
	threshold = None
	
	for o, v in opts :
		if o == "-c" :
			configurationPath = v
		elif o == "-o" :
			outputFolder = v
		elif o == "-k" :
			summarySize = int(v)
		elif o == "-s" :
			stopwordsFile = v
		elif o == "-p" :
			punctuationFile = v
		elif o == "-d" :
			dpatternsFile = v
		elif o == "-t" :
			threshold = int(v)
		else :
			assert False, "Unhandled option"

	if not outputFolder or not configurationPath or not summarySize :
		sys.stderr.write('[ERR] The options -c, -o and -k must be specified\n')
		print usage
		sys.exit(2)

	params = readConfigFile(configurationPath)
	if 'news_folder' not in params :
		sys.stderr.write('[ERR] The configuration file must include the news folder path\nFORMAT:\nnews_folder = ...\n')
		sys.exit(2)

	newsFolder = params['news_folder']
	if not newsFolder.endswith('/') :
		newsFolder += '/'

	if not outputFolder.endswith('/') :
		outputFolder += '/'

	if 'stopwords_file' in params and not stopwordsFile : stopwordsFile = params['stopwords_file']
	with open(stopwordsFile,'r') as f : stopwords = f.read().replace('\n',' ').strip().split()
	if 'punctuation_file' in params and not punctuationFile : punctuationFile = params['punctuation_file']
	with open(punctuationFile,'r') as f : punctuation = f.read().replace('\n',' ').strip().split()
	if 'dpatterns_file' in params and not dpatternsFile : dpatternsFile = params['dpatterns_file']
	with open(dpatternsFile,'r') as f : dpatterns = f.read().replace('\n',' ').strip().split()
	if 'threshold' in params and not threshold : threshold = int(params['threshold'])
	else : threshold = 0

	preprocessor = Preprocessing(stopwords=stopwords, punctuation=punctuation, dpatterns=dpatterns, threshold=threshold)
	summarizeNews(newsFolder,preprocessor,outputFolder,summarySize)	


