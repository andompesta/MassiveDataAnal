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
		for p in self.punctuation :
			document = document.replace(p,' ')

		# apply lowercase and split into words
		document = document.strip().lower().split()

		# transforms the document in a list of tokens satisfying the following rules:
		# - len(t) > 0
		# - t not in Stopword
		# - t doesn't contain any Discard Pattern
		# - # occurrencies of t in document >= Threshold
		for dp in self.dpattern :
			for token in document :
				if dp in token :
					document = filter(lambda x : x != token,document)

		return [token for token in document if token != '' and token not in self.stopwords and document.count(token)>= self.threshold]

f = open('data/sw.txt')
stopwords = f.read().replace('\n',' ').strip().split()
f.close()
f = open('data/punc.txt')
punctuation = f.read().replace('\n',' ').strip().split()
f.close()
Preprocessing(stopwords=stopwords,punctuation=punctuation,threshold=1).save('newsFilter_2.0.pp')