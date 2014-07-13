
import os,json
from preprocess import Preprocessing
from utilities import readConfigFile

def shiftPreproc(inputPath,outputPath,preprocessor) :
	shifts = []
	with open(inputPath) as f :
		shifts = [json.loads(line) for line in f if line != '']
	for shift in shifts :
		for tweet in shift :
			tweet['text'] = ''.join(map(lambda t : t + ' ',preprocessor.processDoc(tweet['text']))).strip()
	with open(outputPath,'w') as f :
		f.write(''.join(map(lambda s: json.dumps(s) + '\n',shifts)).strip())


def tweetPreproc(inputPath,outputPath,preprocessor) :
	tweets = []
	with open(inputPath) as f :
		tweets = json.loads(f.read())
	for tweet in tweets :
		tweet['text'] = ''.join(map(lambda t : t + ' ',preprocessor.processDoc(tweet['text']))).strip()
	with open(outputPath,'w') as f :
		f.write(json.dumps(tweets))

def preprocessShifts(inputFolder,outputFolder,preprocessor) :
	paths = map(lambda x: (inputFolder+x,outputFolder+x), os.listdir(inputFolder))
	for inPath,outPath in paths :
		shiftPreproc(inPath,outPath,preprocessor)


if __name__ == '__main__' :
	
	import getopt
	import sys

	usage = '''PARAMS:
	-c\tConfiguration file path
	-i\tInput folder
	-o\tOutput folder

	-s\tPath of the stopwords file (OPTIONAL)
	-p\tPath of the punctuation file (OPTIONAL)
	-d\tPath of the discard-pattern file (OPTIONAL)
	-t\tThreshold (OPTIONAL)
	'''

	try :
		opts, args = getopt.getopt(sys.argv[1:], "c:o:i:s:p:d:t:")
	except getopt.GetoptError as err :
		sys.stderr.write(str(err) + '\n')
		print usage
		sys.exit(2)

	configurationPath = None
	inputFolder = None
	outputFolder = None

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
		elif o == "-i" :
			inputFolder = v
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

	if not outputFolder or not configurationPath or not inputFolder :
		sys.stderr.write('[ERR] The options -c, -o and -i must be specified\n')
		print usage
		sys.exit(2)

	params = readConfigFile(configurationPath)
	if 'shift_info_folder' not in params or 'shift_tweets_folder' not in params :
		sys.stderr.write('[ERR] The configuration file must include the contradictions info/tweets folders path\nFORMAT:\ncontradictions_info_folder = ...\ncontradictions_tweets_folder = ...\n')
		sys.exit(2)

	if 'tweets_folder' not in params :
		sys.stderr.write('[ERR] The configuration file must include the tweets folder path\nFORMAT:\ntweets_folder = ...\n')
		sys.exit(2)

	if not inputFolder.endswith('/') :
		inputFolder += '/'

	if not outputFolder.endswith('/') :
		outputFolder += '/'

	if 'stopwords_file' in params and stopwordsPath == None : stopwordsPath = params['stopwords_file']
	with open(stopwordsPath,'r') as f : stopwords = f.read().replace('\n',' ').strip().split()
	if 'punctuation_file' in params and punctuationPath == None : punctuationPath = params['punctuation_file']
	with open(punctuationPath,'r') as f : punctuation = f.read().replace('\n',' ').strip().split()
	if 'dpatterns_file' in params and dpatternsPath == None : dpatternsPath = params['dpatterns_file']
	with open(dpatternsPath,'r') as f : dpatterns = f.read().replace('\n',' ').strip().split()
	if 'threshold' in params and threshold == None : threshold = int(params['threshold']); print 'wtf'
	else : threshold = 0

	preprocessor = Preprocessing(stopwords=stopwords, punctuation=punctuation, dpatterns=dpatterns, threshold=threshold, removeURLs=True, removeUnicode=True)
	preprocessShifts(inputFolder,outputFolder,preprocessor)