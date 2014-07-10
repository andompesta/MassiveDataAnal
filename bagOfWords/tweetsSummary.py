import os
import json
from gensim import corpora, models

from preprocess import Preprocessing
from utilities import readConfigFile

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

	for i, path in enumerate(tweetsPaths) :
		print "\rParsing tweets: " + str(int((i/float(len(tweetsPaths)))*100)) + '%',

		with open(path) as f :
			topic = path.split('/')[-1].partition('-')[0]
			topicContr = [json.loads(line.strip()) for line in f if line.strip() != '']
			
			for j in xrange(len(topicContr)) :
				contrText = []

				for t in topicContr[j] :
					contrText.append(' '+t['text'])

				text = ''.join(contrText).strip()
				contradictionList[topic]['contradictions'][j]['text'] = text
				contradictionList[topic]['contradictions'][j]['size'] = len(topicContr)
	
	print '\rParsing tweets: 100%'
	return contradictionList.values()

def summarizeTweets(tweetsFolder,infoFolder,pp,outputFilename,kTerms) :
	contradictionList = readTweetsFiles(tweetsFolder,infoFolder)
	texts = []

	for topic in contradictionList :
		for contr in topic['contradictions'] :
			texts.append( pp.processDoc(contr['text']) )

	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]
	tfidf = models.TfidfModel(corpus)

	for topic in contradictionList :
		for contr in topic['contradictions'] :

			tokens = pp.processDoc(contr['text'])
			bow = dictionary.doc2bow(tokens)
			contr['summary'] = map(lambda x:(dictionary[x[0]],x[1]), sorted(tfidf[bow],key=lambda x:x[1],reverse=True)[:kTerms])
			contr.pop('text')

	with open(outputFilename,'w') as f :
		f.write(json.dumps(contradictionList))

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

	stopwordsPath = None
	punctuationPath = None
	dpatternsPath = None

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
			stopwordsPath = v
		elif o == "-p" :
			punctuationPath = v
		elif o == "-d" :
			dpatternsPath = v
		elif o == "-t" :
			threshold = int(v)
		else :
			assert False, "Unhandled option"

	if not outputFilename or not configurationPath or not summarySize :
		sys.stderr.write('[ERR] The options -c, -o and -k must be specified\n')
		print usage
		sys.exit(2)

	params = readConfigFile(configurationPath)
	if 'contradictions_info_folder' not in params or 'contradictions_tweets_folder' not in params :
		sys.stderr.write('[ERR] The configuration file must include the contradictions info and tweets folders path\nFORMAT:\ncontradictions_info_folder = ...\ncontradictions_tweets_folder = ...\n')
		sys.exit(2)

	infoFolder = params['contradictions_info_folder']
	if not infoFolder.endswith('/') :
		infoFolder += '/'
	tweetsFolder = params['contradictions_tweets_folder']
	if not tweetsFolder.endswith('/') :
		tweetsFolder += '/'

	if 'stopwords_file' in params and not stopwordsPath : stopwordsPath = params['stopwords_file']
	with open(stopwordsPath,'r') as f : stopwords = f.read().replace('\n',' ').strip().split()
	if 'punctuation_file' in params and not punctuationPath : punctuationPath = params['punctuation_file']
	with open(punctuationPath,'r') as f : punctuation = f.read().replace('\n',' ').strip().split()
	if 'dpatterns_file' in params and not dpatternsPath : dpatternsPath = params['dpatterns_file']
	with open(dpatternsPath,'r') as f : dpatterns = f.read().replace('\n',' ').strip().split()
	if 'threshold' in params and not threshold : threshold = int(params['threshold'])
	else : threshold = 0

	preprocessor = Preprocessing(stopwords=stopwords, punctuation=punctuation, dpatterns=dpatterns, threshold=threshold)
	summarizeTweets(tweetsFolder,infoFolder,preprocessor,outputFilename,summarySize)	
