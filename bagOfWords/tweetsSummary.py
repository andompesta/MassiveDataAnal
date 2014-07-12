import os
import json
from gensim import corpora, models

from preprocess import Preprocessing
from utilities import readConfigFile

def readShiftFiles(shiftTweetsFolder,shiftInfoFolder) :
	
	# reads the contradiction info files
	shiftList = {}
	shiftInfoPaths = map(lambda x: shiftInfoFolder+x, os.listdir(shiftInfoFolder))
	for path in shiftInfoPaths :
		topic = path.split('/')[-1].partition('.')[0]
		
		with open(path,'r') as f :
			infoJson = json.loads(f.read())
			shiftList[topic] = infoJson['contradictions']

	# reads the contradiction tweets files
	shiftTweetsPaths = map(lambda x: shiftTweetsFolder+x, os.listdir(shiftTweetsFolder))

	for i, path in enumerate(shiftTweetsPaths) :		

		with open(path) as f :
			topic = path.split('/')[-1].partition('-')[0]
			topicContr = [json.loads(line.strip()) for line in f if line.strip() != '']
			
			for j in xrange(len(topicContr)) :
				contrText = []

				for t in topicContr[j] :
					contrText.append(' '+t['text'])

				text = ''.join(contrText).strip()
				shiftList[topic][j]['text'] = text
				shiftList[topic][j]['size'] = len(topicContr[j])
		
	return shiftList

def readTweetsFiles(tweetsFolder) :
	tweets = {}
	tweetsPaths = map(lambda x: tweetsFolder+x, os.listdir(tweetsFolder))
	for path in tweetsPaths :
		topic = path.split('/')[-1].partition('.')[0]
		with open(path,'r') as f :
			tweets[topic]= json.loads(f.read())

	return tweets


def summarizeTweets(tweetsFolder,shiftTweetsFolder,shiftInfoFolder,pp,outputFilename,kTerms) :
	shiftList = readShiftFiles(shiftTweetsFolder,shiftInfoFolder)
	tweets = readTweetsFiles(tweetsFolder)

	baselines = {}
	tfidfModels = {}
	for topic in tweets :
		baselines[topic] = []
		for t in tweets[topic] :
			baselines[topic].append( pp.processDoc(t['text']) )

	dictionary = corpora.Dictionary([tweet for topic in baselines for tweet in baselines[topic]])

	for topic in set(shiftList).intersection(set(tweets)) :
		
		corpus = [dictionary.doc2bow(text) for text in baselines[topic]]
		tfidf = models.TfidfModel(corpus)
		
		for contr in shiftList[topic] :

			tokens = pp.processDoc(contr['text'])
			bow = dictionary.doc2bow(tokens)
			contr['summary'] = map(lambda x:(dictionary[x[0]],x[1]), sorted(tfidf[bow],key=lambda x:x[1],reverse=True)[:kTerms])
			contr.pop('text')

	for topic in set(shiftList)-set(tweets) :
		shiftList.pop(topic)

	with open(outputFilename,'w') as f :
		f.write(json.dumps(shiftList))

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
	if 'shift_info_folder' not in params or 'shift_tweets_folder' not in params :
		sys.stderr.write('[ERR] The configuration file must include the contradictions info/tweets folders path\nFORMAT:\ncontradictions_info_folder = ...\ncontradictions_tweets_folder = ...\n')
		sys.exit(2)

	if 'tweets_folder' not in params :
		sys.stderr.write('[ERR] The configuration file must include the tweets folder path\nFORMAT:\ntweets_folder = ...\n')
		sys.exit(2)

	shiftInfoFolder = params['shift_info_folder']
	if not shiftInfoFolder.endswith('/') :
		shiftInfoFolder += '/'
	shiftTweetsFolder = params['shift_tweets_folder']
	if not shiftTweetsFolder.endswith('/') :
		shiftTweetsFolder += '/'
	tweetsFolder = params['tweets_folder']
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
	summarizeTweets(tweetsFolder,shiftTweetsFolder,shiftInfoFolder,preprocessor,outputFilename,summarySize)	
