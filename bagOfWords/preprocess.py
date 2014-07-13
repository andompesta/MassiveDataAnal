import pickle
import re 

class Preprocessing :

	def __init__(self,stopwords={},punctuation={},dpatterns={},threshold=0,removeURLs=True,removeUnicode=False) :
		'''
		Constructor for the Preprocessing instance. Optional args:
		- stopwords = a set of stopwords to be excluded by the filtering.
		- punctuation = a set of characters to be replaced with a whitespace.
		- dpatterns = a set of string patterns. if a pattern is a substring of a token, the token is discarded.
		- threshold = a positive integer threshold to discard the less frequent tokens in the document.

		'''
		self.stopwords = {sw.lower() for sw in stopwords}
		self.punctuation = punctuation
		self.dpatterns = dpatterns
		self.threshold = threshold
		self.removeURLs = removeURLs
		self.removeUnicode = removeUnicode

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

	@staticmethod
	def removeURL(document) :
		return re.sub(r'https?:\/\/[A-Za-z0-9\.\/]*', '', document, flags=re.MULTILINE)

	@staticmethod
	def removeUnicode(document) :
		return document.encode('ascii','ignore')


	def processDoc(self,document):
		'''
		Given a document as a string, preprocesses it returning a list of tokens (strings).

		'''
		# removes URLs
		if self.removeURLs :
			document = Preprocessing.removeURL(document)
		if self.removeUnicode :
			document = Preprocessing.removeUnicode(document)

		# removes punctuation
		for p in self.punctuation :
			document = document.replace(p,' ')

		# applies lowercase and split into words
		document = document.strip().lower().split()

		# discard patterns filtering
		for dp in self.dpatterns :
			document = filter(lambda token : not dp in token,document)

		# threshold filtering
		counter = {}
		for token in document :
			if not token in counter : counter[token] = 1
			else : counter[token] += 1
		document = [t for t in document if counter[t] >= self.threshold]

		# stopwords filtering
		return [token for token in document if token not in self.stopwords and token != '']


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
		opts, args = getopt.getopt(sys.argv[1 :], "o:s:p:d:t:")
	except getopt.GetoptError as err :
		sys.stderr.write(str(err) + '\n')
		print usage
		sys.exit(2)

	outputFilename = None
	stopwords = set()
	punctuation = set()
	dpatterns = set()
	threshold = 0

	for o, v in opts :
		if o == "-o" :
			outputFilename = v
		elif o == "-s" :
			with open(v,'r') as f : stopwords = f.read().replace('\n',' ').strip().split()
		elif o == "-p" :
			with open(v,'r') as f : punctuation = f.read().replace('\n',' ').strip().split()
		elif o == "-d" :
			with open(v,'r') as f : dpatterns = f.read().replace('\n',' ').strip().split()	
		elif o == "-t" :
			threshold = int(v)
		else :
			assert False, "Unhandled option"

	if not outputFilename :
		sys.stderr.write('[ERR] The option -o must be specified\n')
		print usage
		sys.exit(2)

	Preprocessing(stopwords=stopwords,punctuation=punctuation,dpatterns=dpatterns,threshold=threshold).save(outputFilename)
