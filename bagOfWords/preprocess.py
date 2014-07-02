import pickle

def defaultFilter(document,word) :
	return True

class Preprocessing :

	def __init__(self,stopwords={},punctuation={},flter=defaultFilter) :
		'''
		Constructor for the Preprocessing instance. Optional args:
		- stopwords = a set of stopwords to be excluded by the filtering.
		- punctuation = a set of characters to be replaced with a whitespace.
		- flter = a filtering function f: [String] -> String -> Bool taking as arguments the document and the current word.

		'''
		self.stopwords = {sw.lower() for sw in stopwords}
		self.punctuation = punctuation
		self.filter = flter

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
		# - t not in Stopwords
		# - filter(t) = True
		return [word for word in document if word != '' and word not in self.stopwords and self.filter(document,word)]

