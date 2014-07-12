import os
import json
from gensim import corpora, models

from preprocess import Preprocessing
from utilities import readConfigFile

def readShiftFile(shiftTweetsPath,shiftInfoPath) :

	shiftList = None
	with open(shiftInfoPath) as f :
		infoJson = json.loads(f.read())
		shiftList = infoJson['contradictions']

	with open(shiftTweetsPath) as f :
		topicContr = [json.loads(line.strip()) for line in f if line.strip() != '']

		for i in xrange(len(topicContr)) :
			contrText = []

			for t in topicContr[i] :
				contrText.append(' '+t['text'])

			text = ''.join(contrText).strip()
			shiftList[i]['text'] = text
			shiftList[i]['size'] = len(topicContr[i])
				
	return shiftList

def summarizeTweets(tweetsFolder,shiftTweetsFolder,shiftInfoFolder,pp,outputFolder,kTerms) :

	tweetsPaths = dict(map(lambda x: ((tweetsFolder+x).split('/')[-1].partition('.')[0],tweetsFolder+x), os.listdir(tweetsFolder)))
	shiftInfoPaths = dict(map(lambda x: ((shiftInfoFolder+x).split('/')[-1].partition('.')[0],shiftInfoFolder+x), os.listdir(shiftInfoFolder)))
	shiftTweetsPaths = dict(map(lambda x: ((shiftTweetsFolder+x).split('/')[-1].partition('-')[0],shiftTweetsFolder+x), os.listdir(shiftTweetsFolder)))

	for topic in set(tweetsPaths).intersection(set(shiftInfoPaths)).intersection(set(shiftTweetsPaths)) :
		
		with open(tweetsPaths[topic]) as f :
			tweets = json.loads(f.read())
		
		shiftList = readShiftFile(shiftTweetsPaths[topic],shiftInfoPaths[topic])

		baseline = []
		
		for t in tweets :
			baseline.append( pp.processDoc(t['text']) )

		dictionary = corpora.Dictionary(baseline)
		corpus = [dictionary.doc2bow(text) for text in baseline]
		tfidf = models.TfidfModel(corpus)
		
		for contr in shiftList :

			tokens = pp.processDoc(contr['text'])
			bow = dictionary.doc2bow(tokens)
			contr['summary'] = map(lambda x:(dictionary[x[0]],x[1]), sorted(tfidf[bow],key=lambda x:x[1],reverse=True)[:kTerms])
			contr.pop('text')

		with open(outputFolder + topic + '.json','w') as f :
			f.write(json.dumps(shiftList))

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
			outputFolder = v
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

	if not outputFolder or not configurationPath or not summarySize :
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

	if not outputFolder.endswith('/') :
		outputFolder += '/'

	if 'stopwords_file' in params and not stopwordsPath : stopwordsPath = params['stopwords_file']
	with open(stopwordsPath,'r') as f : stopwords = f.read().replace('\n',' ').strip().split()
	if 'punctuation_file' in params and not punctuationPath : punctuationPath = params['punctuation_file']
	with open(punctuationPath,'r') as f : punctuation = f.read().replace('\n',' ').strip().split()
	if 'dpatterns_file' in params and not dpatternsPath : dpatternsPath = params['dpatterns_file']
	with open(dpatternsPath,'r') as f : dpatterns = f.read().replace('\n',' ').strip().split()
	if 'threshold' in params and not threshold : threshold = int(params['threshold'])
	else : threshold = 0

	preprocessor = Preprocessing(stopwords=stopwords, punctuation=punctuation, dpatterns=dpatterns, threshold=threshold)
	summarizeTweets(tweetsFolder,shiftTweetsFolder,shiftInfoFolder,preprocessor,outputFolder,summarySize)	
