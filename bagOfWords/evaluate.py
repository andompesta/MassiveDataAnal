import json

from tweetsSummary import readShiftFiles
from newsSummary import readNewsFiles
from preprocess import Preprocessing
from utilities import readConfigFile,unixTime,readableDatetime

def readSimilarityFile(path) :
	with open(path,'r') as f :
		similarities = json.loads(f.read())
		return similarities

def readNewsSummaryFile(path) :
	with open(path,'r') as f :
		#newsSum = dict( map(lambda t : (t['topic'],dict(map(lambda a: (a['_id']['$oid'],a['summary']),t['articles']))),json.loads(f.read())))
		return json.loads(f.read())
		
def readShiftSummaryFile(path) :
	with open(path,'r') as f :
		return json.loads(f.read())


def evaluate(newsPath,shiftSumPath,newsSumPath,similPath, outputFolder) :

	news = readNewsFiles(newsPath)
	shiftSum = readShiftSummaryFile(shiftSumPath)
	newsSum = readNewsSummaryFile(newsSumPath)
	similarities = readSimilarityFile(similPath)

	

	for topic in set(similarities).intersection(set(newsSum)).intersection(set(shiftSum)).intersection(set(news)) :
	#for topic in ['Cern','Lcross','MichaelJackson','Hangover'] :
	

		evaluation = '--------------------------------------------------------\n'
		evaluation += topic + '\n'
		for i in xrange(len(similarities[topic])) :

			evaluation += '--------------------------------------------------------\n'
			evaluation += 'FROM: ' + similarities[topic][i]['timeBegin'] + ' TO : ' + similarities[topic][i]['timeEnd'] + '\n'
			evaluation += 'NUMBER OF TWEETS: ' + str(similarities[topic][i]['size']) + '\n'
			evaluation += 'SHIFT SUMMARY: ' + ''.join(map(lambda x : x[0]+' ',shiftSum[topic][i]['summary']) ) + '\n'
			# evaluation += some random tweets of the contradiction

			if similarities[topic][i]['correlations'] != [] :
				bestNewsId = similarities[topic][i]['correlations'][0]['_id']
				evaluation += '\nBest news over ' + str(len(similarities[topic][i]['correlations'])) + ' candidates:' + '\n'
				evaluation += '\tNEWS ID: ' + bestNewsId + ' NEWS DATE: ' + newsSum[topic][bestNewsId]['pub_date'] + '\n'
				evaluation += '\tNEWS SUMMARY: ' + ''.join(map(lambda x : x[0]+' ',newsSum[topic][bestNewsId]['summary'])) + '\n'
				evaluation += '\tFIRST PARAGRAPH: ' + ''.join(news[topic][bestNewsId]['full_text'].split('\n')[:3]) + '\n'

				# evaluation += the first lines of the news that correlates the most, with data, score, etc..
				# evaluation += the news summary
			else : evaluation += '\nNo match found' + '\n'
		evaluation += '\n'

		with open(outputFolder+'eval_'+topic+'.txt','w') as f :
			f.write(evaluation.encode('utf-8'))

fldr = 'data/results/'
evaluate('data/news/',fldr+'shiftSummary.json',fldr+'newsSummary.json',fldr+'similarities.json',fldr+'evals/')