from gensim import corpora, models, similarities

from tweetsSummary import readTweetsFiles
from newsSummary import readNewsFiles
from preprocess import Preprocessing
from utilities import readConfigFile,unixTime

def computeCorrelation(newsFolder,tweetsFolder,infoFolder,preprocessor,outputFilename,lsiDimensions) :
	news = dict(map(lambda j : (j['topic'],j['articles']), readNewsFiles(newsFolder)))
	contradictions = dict(map(lambda j : (j['topic'],j['contradictions']), readTweetsFiles(tweetsFolder,infoFolder)))
	
	# tokenizes every text and creates the dictionary
	print "[Tokenizing]"
	everyDocument = []
	for topic in news :
		for article in news[topic] :
			article['tokens'] = preprocessor.processDoc(article['full_text'])
			article.pop('full_text')

			article['pub_date'] = unixTime(article['pub_date']) # also converts articles pub date in seconds from Epoch
			everyDocument.append( article['tokens'] )

	for topic in contradictions :
		for contr in contradictions[topic] :
			contr['tokens'] = preprocessor.processDoc(contr['text'])
			contr.pop('text')
			everyDocument.append( contr['tokens'] )
	
	print "Number of documents: " + str(len(everyDocument))
	print "Number of tokens: " + str(sum(map(len,everyDocument)))
	print "Number of characters: " + str(sum(map(lambda doc : sum(map(len,doc)),everyDocument)))

	print "[Generating dictionary]"
	dictionary = corpora.Dictionary(everyDocument)

	# drops the token representation for each document, replacing it with bag-of-words
	for topic in news :
		for article in news[topic] :
			article['bow'] = dictionary.doc2bow(article['tokens'])
			article.pop('tokens')

	for topic in contradictions :
		for contr in contradictions[topic] :
			contr['bow'] = dictionary.doc2bow(contr['tokens'])
			contr.pop('tokens')

	print "[Converting the documents to bow]"
	everyDocument = map(lambda d : dictionary.doc2bow(d), everyDocument)

	# big models
	print "[Training the TF-IDF model]"
	tfidfTOT = models.TfidfModel(everyDocument)
	print "[Training the LSI model]"
	print "Number of dimensions: " + str(lsiDimensions)
	lsi = models.LsiModel(tfidfTOT[everyDocument], id2word=dictionary, num_topics=lsiDimensions)

	print "[Calculating similarities]"
	#for topic in contradictions :
	for topic in ['Cern','MichaelJackson'] :
		for contr in contradictions[topic] :
			tBegin = contr['timeBegin']
			tEnd = contr['timeEnd']
			size = contr['size']

			# trains the transformation model using all the topic news
			#corpus_bow = [n['bow'] for n in news[topic]]
			#lsi = models.LsiModel(corpus_bow, id2word=dictionary, num_topics=lsiDimensions)

			# selects the candidate news for the index
			span = 24 * 3600 * size / 10 # to be tested!
			candidateNews = [n for n in news[topic] if n['pub_date'] <= tEnd and n['pub_date'] >= tBegin - span]

			# generates a Latent Semantic Index with the candidate news
			candidate_bow = [n['bow'] for n in candidateNews]
			if candidate_bow != [] :
				index = similarities.MatrixSimilarity(lsi[candidate_bow])

				# test the contradiction text on the index
				sim = sorted(enumerate(index[lsi[contr['bow']]]), key=lambda x: -x[1])
				

				# SUMMARIES GENERATED WITH TF-IDF ON THE WHOLE CORPUS
				shiftSumTOT = map(lambda x : dictionary[x[0]], sorted(tfidfTOT[contr['bow']],key=lambda x:x[1],reverse=True)[:10])								
				newsSumTOT = map(lambda x : dictionary[x[0]], sorted(tfidfTOT[candidate_bow[sim[0][0]]],key=lambda x:x[1],reverse=True)[:10])				

				# SUMMARIES GENERATED WITH TF-IDF ON THE WHOLE TOPIC
				tfidfTOP = models.TfidfModel([n['bow'] for n in news[topic]]+[c['bow'] for c in contradictions[topic]])

				shiftSumTOP = map(lambda x : dictionary[x[0]], sorted(tfidfTOP[contr['bow']],key=lambda x:x[1],reverse=True)[:10])						
				newsSumTOP = map(lambda x : dictionary[x[0]], sorted(tfidfTOP[candidate_bow[sim[0][0]]],key=lambda x:x[1],reverse=True)[:10])				

				# SUMMARIES GENERATED WITH DIFFERENT TF-IDF FOR NEWS AND TWEETS
				tfidfSHIFT = models.TfidfModel([c['bow'] for topic in ['Cern','MichaelJackson'] for c in contradictions[topic]])
				tfidfNEWS = models.TfidfModel([n['bow'] for topic in ['Cern','MichaelJackson'] for n in news[topic]])

				shiftSumDIF = map(lambda x : dictionary[x[0]], sorted(tfidfSHIFT[contr['bow']],key=lambda x:x[1],reverse=True)[:10])								
				newsSumDIF = map(lambda x : dictionary[x[0]], sorted(tfidfNEWS[candidate_bow[sim[0][0]]],key=lambda x:x[1],reverse=True)[:10])				

				print "Shift summary (TOTAL): " + str(shiftSumTOT)
				print "Shift summary (TOPIC): " + str(shiftSumTOP)
				print "Shift summary (DIFFERENT): " + str(shiftSumDIF)
				print "Most similar news (TOTAL): " + str(newsSumTOT)
				print "Most similar news (TOPIC): " + str(newsSumTOP)
				print "Most similar news (DIFFERENT): " + str(newsSumDIF)

def readConfigFile(path) :
	with open(path,'r') as f :
		lines = [l for l in f if l != '' and l[0] != '#']
		params = map(lambda t : (t[0].strip(),t[-1].strip()), map(lambda l : l.partition('='),lines))
		return dict(params)

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

	if 'contradictions_info_folder' not in params or 'contradictions_tweets_folder' not in params :
		sys.stderr.write('[ERR] The configuration file must include the contradictions info and tweets folders path\nFORMAT:\ncontradictions_info_folder = ...\ncontradictions_tweets_folder = ...\n')
		sys.exit(2)

	newsFolder = params['news_folder']
	if not newsFolder.endswith('/') :
		newsFolder += '/'

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
	computeCorrelation(newsFolder,tweetsFolder,infoFolder,preprocessor,outputFilename,lsiDimensions)	
