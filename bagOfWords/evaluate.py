import json,os

from tweetsSummary import readShiftFile
from newsSummary import readNewsFile
from preprocess import Preprocessing
from utilities import readConfigFile,unixTime,readableDatetime

def evaluate(newsFolder,shiftSumFolder,newsSumFolder,similFolder, outputFolder) :

	newsPaths = dict(map(lambda x: ((newsFolder+x).split('/')[-1].partition('.')[0].partition('_')[-1],newsFolder+x), os.listdir(newsFolder)))
	newsSumPaths = dict(map(lambda x: ((newsSumFolder+x).split('/')[-1].partition('.')[0],newsSumFolder+x), os.listdir(newsSumFolder)))
	shiftSumPaths = dict(map(lambda x: ((shiftSumFolder+x).split('/')[-1].partition('.')[0],shiftSumFolder+x), os.listdir(shiftSumFolder)))
	similPaths = dict(map(lambda x: ((similFolder+x).split('/')[-1].partition('.')[0],similFolder+x), os.listdir(similFolder)))

	for topic in set(newsPaths).intersection(set(newsSumPaths)).intersection(set(shiftSumPaths)).intersection(set(similPaths)) :

		news = readNewsFile(newsPaths[topic])
		with open(newsSumPaths[topic],'r') as f :
			newsSum = json.loads(f.read())
		with open(shiftSumPaths[topic],'r') as f :
			shiftSum = json.loads(f.read())
		with open(similPaths[topic],'r') as f :
			simil = json.loads(f.read())
		
		evaluation = '--------------------------------------------------------\n'
		evaluation += topic + '\n'
		for i in xrange(len(simil)) :

			evaluation += '--------------------------------------------------------\n'
			evaluation += 'FROM: ' + simil[i]['timeBegin'] + ' TO : ' + simil[i]['timeEnd'] + '\n'
			evaluation += 'NUMBER OF TWEETS: ' + str(simil[i]['size']) + '\n'
			evaluation += 'SHIFT SUMMARY: ' + ''.join(map(lambda x : x[0]+' ',shiftSum[i]['summary']) ) + '\n'
			# evaluation += some random tweets of the contradiction

			if simil[i]['correlations'] != [] :
				bestNewsId = simil[i]['correlations'][0]['_id']
				evaluation += '\nBest news over ' + str(len(simil[i]['correlations'])) + ' candidates:' + '\n'
				evaluation += '\tNEWS ID: ' + bestNewsId + ' NEWS DATE: ' + newsSum[bestNewsId]['pub_date'] + '\n'
				evaluation += '\tNEWS SUMMARY: ' + ''.join(map(lambda x : x[0]+' ',newsSum[bestNewsId]['summary'])) + '\n'
				evaluation += '\tFIRST PARAGRAPH: ' + ''.join(news[bestNewsId]['full_text'].split('\n')[:3]) + '\n'

				# evaluation += the first lines of the news that correlates the most, with data, score, etc..
				# evaluation += the news summary
			else : evaluation += '\nNo match found' + '\n'
		evaluation += '\n'

		with open(outputFolder+'eval_'+topic+'.txt','w') as f :
			f.write(evaluation.encode('utf-8'))

fldr = 'data/results/'
evaluate('data/news/',fldr+'shiftSummaries/',fldr+'newsSummaries/',fldr+'similarities/',fldr+'evals/')