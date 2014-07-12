from gensim import corpora, models, similarities
import json

from tweetsSummary import readShiftFile
from newsSummary import readNewsFile
from preprocess import Preprocessing
from utilities import readConfigFile,unixTime,readableDatetime

def computeCorrelation(newsFolder,tweetsFolder,shiftTweetsFolder,shiftInfoFolder,preprocessor,outputFilename,lsiDimensions) :
	
	print '[Parsing data]'

	newsPaths = map(lambda x: newsFolder+x, os.listdir(newsFolder))
	shiftInfoPaths = dict(map(lambda x: ((shiftInfoFolder+x).split('/')[-1].partition('.')[0],shiftInfoFolder+x), os.listdir(shiftInfoFolder)))
	shiftTweetsPaths = dict(map(lambda x: ((shiftTweetsFolder+x).split('/')[-1].partition('-')[0],shiftTweetsFolder+x), os.listdir(shiftTweetsFolder)))



	news = readNewsFile(newsFolder)
	contradictions = readShiftFile(shiftTweetsFolder,shiftInfoFolder)

	correlations = {}
	
	for topic in set(contradictions).intersection(set(news)) :
		print '[Processing] ' + topic
		correlations[topic] = []
		trainingData = []
		dictionary = corpora.Dictionary()
		
		for artId in news[topic] :
			news[topic][artId]['bow'] = dictionary.doc2bow(preprocessor.processDoc(news[topic][artId]['full_text']),allow_update = True)
			news[topic][artId].pop('full_text')
			trainingData.append(news[topic][artId]['bow'])


		for contr in contradictions[topic] :
			tBegin = contr['timeBegin']
			tEnd = contr['timeEnd']
			size = contr['size']

			bow = dictionary.doc2bow(preprocessor.processDoc(contr['text']),allow_update = True)
			lsi = models.LsiModel(trainingData, id2word=dictionary, num_topics=lsiDimensions)

			# selects the candidate news for the index
			# span = int(24 * 3600 * size / 10) # to be tested!
			span = (tEnd - tBegin)*2 # to be tested!
			candidateNews = [{'bow':news[topic][artId]['bow'],'_id':artId} for artId in news[topic] if unixTime(news[topic][artId]['pub_date']) <= tEnd and unixTime(news[topic][artId]['pub_date']) >= tBegin - span]

			# generates a Latent Semantic Index with the candidate news
			if candidateNews != [] :
				index = similarities.MatrixSimilarity(lsi[[n['bow'] for n in candidateNews]])

				# test the contradiction text on the index
				sim = sorted(enumerate(index[lsi[bow]]), key=lambda x: -x[1])

				for i,s in sim :
					candidateNews[i]['val'] = float(s)
					candidateNews[i].pop('bow')

				candidateNews.sort(key=lambda n : n['val'], reverse = True)

			outcontr = {'timeBegin' : readableDatetime(tBegin), 'timeEnd' : readableDatetime(tEnd), 'size' : size, 'correlations' : candidateNews}
			correlations[topic].append(outcontr)

	with open(outputFilename,'w') as f :
		f.write(json.dumps(correlations))

if __name__ == '__main__' :
	import getopt
	import sys

	usage = '''PARAMS:
	-c\tConfiguration file path
	-o\tOutput filename
	-l\tLSI space size

	-s\tPath of the stopwords file (OPTIONAL)
	-p\tPath of the punctuation file (OPTIONAL)
	-d\tPath of the discard-pattern file (OPTIONAL)
	-t\tThreshold (OPTIONAL)
	'''

	try :
		opts, args = getopt.getopt(sys.argv[1:], "c:o:l:s:p:d:t:")
	except getopt.GetoptError as err :
		sys.stderr.write(str(err) + '\n')
		print usage
		sys.exit(2)

	configurationPath = None
	outputFilename = None
	lsiDimensions = None

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
		elif o == "-l" :
			lsiDimensions = int(v)
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

	if not outputFilename or not configurationPath or not lsiDimensions :
		sys.stderr.write('[ERR] The options -c, -o and -l must be specified\n')
		print usage
		sys.exit(2)

	params = readConfigFile(configurationPath)
	if 'news_folder' not in params :
		sys.stderr.write('[ERR] The configuration file must include the news folder path\nFORMAT:\nnews_folder = ...\n')
		sys.exit(2)

	if 'tweets_folder' not in params :
		sys.stderr.write('[ERR] The configuration file must include the news folder path\nFORMAT:\ntweets_folder = ...\n')
		sys.exit(2)


	if 'shift_info_folder' not in params or 'shift_tweets_folder' not in params :
		sys.stderr.write('[ERR] The configuration file must include the contradictions info and tweets folders path\nFORMAT:\nshift_info_folder = ...\nshift_tweets_folder = ...\n')
		sys.exit(2)

	newsFolder = params['news_folder']
	if not newsFolder.endswith('/') :
		newsFolder += '/'

	tweetsFolder = params['tweets_folder']
	if not tweetsFolder.endswith('/') :
		tweetsFolder += '/'

	shiftInfoFolder = params['shift_info_folder']
	if not shiftInfoFolder.endswith('/') :
		shiftInfoFolder += '/'
	
	shiftTweetsFolder = params['shift_tweets_folder']
	if not shiftTweetsFolder.endswith('/') :
		shiftTweetsFolder += '/'

	if 'stopwords_file' in params and not stopwordsPath : stopwordsPath = params['stopwords_file']
	with open(stopwordsPath,'r') as f : stopwords = f.read().replace('\n',' ').strip().split()
	if 'punctuation_file' in params and not punctuationPath : punctuationPath = params['punctuation_file']
	with open(punctuationPath,'r') as f : punctuation = f.read().replace('\n',' ').strip().split()
	if 'dpatterns_file' in params and not dpatternsPath : dpatternsPath = params['dpatterns_file']
	with open(dpatternsPath,'r') as f : dpatterns = f.read().replace('\n',' ').strip().split()
	if 'threshold' in params and not threshold : threshold = int(params['threshold'])
	else : threshold = 0

	preprocessor = Preprocessing(stopwords=stopwords, punctuation=punctuation, dpatterns=dpatterns, threshold=threshold)
	computeCorrelation(newsFolder,tweetsFolder,shiftTweetsFolder,shiftInfoFolder,preprocessor,outputFilename,lsiDimensions)	
