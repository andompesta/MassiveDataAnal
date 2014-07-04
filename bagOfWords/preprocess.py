import pickle

class Preprocessing :

	def __init__(self,stopwords={},punctuation={},dpattern={},threshold=0) :
		'''
		Constructor for the Preprocessing instance. Optional args:
		- stopwords = a set of stopwords to be excluded by the filtering.
		- punctuation = a set of characters to be replaced with a whitespace.
		- dpattern = a set of string patterns. if a pattern is a substring of a token, the token is discarded.
		- threshold = a positive integer threshold to discard the less frequent tokens in the document.

		'''
		self.stopwords = {sw.lower() for sw in stopwords}
		self.punctuation = punctuation
		self.dpattern = dpattern
		self.threshold = threshold

	def save(self,path) :
		'''
		Given a file path, serializes the Preprocessing instance in a file.

		'''
		f = open(path,'w')
		pickle.dump(self,f)
		f.close()

	@staticmethod
	def load(path) :
		'''
		Static method returning a Preprocessing instance given a file path.
		
		'''
		f = open(path,'r')
		return pickle.load(f)

	def processDoc(self,document):
		'''
		Given a document as a string, preprocesses it returning a list of tokens (strings).

		'''
		# removes punctuation
		print 'removing punctuation'
		for p in self.punctuation :
			document = document.replace(p,' ')

		# apply lowercase and split into words
		print 'splitting'
		document = document.strip().lower().split()

		# transforms the document in a list of tokens satisfying the following rules:
		# - len(t) > 0
		# - t not in Stopword
		# - t doesn't contain any Discard Pattern
		# - # occurrencies of t in document >= Threshold
		print 'discard-pattern phase -- size: ' + str(len(document)) 
		for dp in self.dpattern :
			for token in document :
				if dp in token :
					document = filter(lambda x : x != token,document)

		print 'stopwords and threshold phase -- size: ' + str(len(document))
		counter = {}
		for token in document :
			if not token in counter : counter[token] = 1
			else : counter[token] += 1
		document = [t for t in document if counter[t] > self.threshold]

		return [token for token in document if token != '' and token not in self.stopwords]

if __name__ == '__main__' :
	import getopt
	import sys
	
	usage = '''PARAMS :
	-o\tOutput file
	-s\tPath of the stopwords file (OPTIONAL)
	-p\tPath of the punctuation file (OPTIONAL)
	-d\tPath of the discard-pattern file (OPTIONAL)
	-t\tThreshold (OPTIONAL)
	'''

	try :
		opts, args = getopt.getopt(sys.argv[1 :], "o:s:p:d:t")
	except getopt.GetoptError as err :
		sys.stderr.write(str(err) + '\n')
		print usage
		sys.exit(2)

	outputFilename = None
	stopwords = set()
	punctuation = set()
	dpattern = set()
	threshold = 0

	for o, v in opts :
		if o == "-o" :
			outputFilename = v
		elif o == "-s" :
			with open(v,'r') as f : stopwords = f.read().replace('\n',' ').strip().split()
		elif o == "-p" :
			with open(v,'r') as f : punctuation = f.read().replace('\n',' ').strip().split()
		elif o == "-d" :
			with open(v,'r') as f : dpattern = f.read().replace('\n',' ').strip().split()	
		elif o == "-t" :
			threshold = int(v)
		else :
			assert False, "Unhandled option"

		if not outputFilename :
			sys.stderr.write('[ERR] The option -o must be specified\n')
			print usage
			sys.exit(2)

	Preprocessing(stopwords=stopwords,punctuation=punctuation,dpattern=dpattern,threshold=threshold).save(outputFilename)
