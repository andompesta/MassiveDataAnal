import os
import json
from gensim import corpora, models

from preprocess import Preprocessing
from utilities import readConfigFile

def readNewsFiles(folder) :
	news = {}
	paths = map(lambda x: folder+x, os.listdir(folder))
	i = 0
	
	for path in paths :
		print "\rParsing news: " + str(int((i/float(len(paths)))*100)) + '%',
		with open(path) as f :
			topicJson = json.loads(f.read())
			topic = topicJson['topic']
			news[topic] = {'topic' : topic, 'articles' : []}
			for article in topicJson['articles'] :
				newFormat = {'_id' : article['_id'], 'pub_date' : article['pub_date'], 'full_text' : article['full_text']}
				news[topic]['articles'].append(newFormat)
		i += 1

	print '\rParsing news: 100%'
	return news.values()

def summarizeNews(newsFolder,pp,outputFilename,kTerms) :
	news = readNewsFiles(newsFolder)
	texts = []
	
	#texts = map(lambda x: pp.processDoc(x[-1]),news)
	
	for topic in news :
		for article in topic['articles'] :
			texts.append(pp.processDoc(article['full_text']))

	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]
	tfidf = models.TfidfModel(corpus)
	output = []

	for topic in news :
		for article in topic['articles'] :
			tokens = pp.processDoc(article['full_text'])
			bow = dictionary.doc2bow(tokens)
			summary = map(lambda x:(dictionary[x[0]],x[1]), sorted(tfidf[bow],key=lambda x:x[1],reverse=True)[:kTerms])
			article['summary'] = summary
			article.pop('full_text')

	with open(outputFilename,'w') as f :
		f.write(json.dumps(news))

if __name__ == '__main__' :
	import getopt
	import sys

	usage = '''PARAMS:
	-c\tConfiguration file path
	-o\tOutput filename
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
	outputFilename = None
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
			outputFilename = v
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

	if not outputFilename or not configurationPath or not summarySize :
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
	if 'stopwords_file' in params and not stopwordsFile : stopwordsFile = params['stopwords_file']
	with open(stopwordsFile,'r') as f : stopwords = f.read().replace('\n',' ').strip().split()
	if 'punctuation_file' in params and not punctuationFile : punctuationFile = params['punctuation_file']
	with open(punctuationFile,'r') as f : punctuation = f.read().replace('\n',' ').strip().split()
	if 'dpatterns_file' in params and not dpatternsFile : dpatternsFile = params['dpatterns_file']
	with open(dpatternsFile,'r') as f : dpatterns = f.read().replace('\n',' ').strip().split()
	if 'threshold' in params and not threshold : threshold = int(params['threshold'])
	else : threshold = 0

	preprocessor = Preprocessing(stopwords=stopwords, punctuation=punctuation, dpatterns=dpatterns, threshold=threshold)
	summarizeNews(newsFolder,preprocessor,outputFilename,summarySize)	


