import os,json

def formatNews(folder) :
	paths = map(lambda x: folder+x, os.listdir(folder))
	i = 0
	newJsons = []
	for path in paths :

		os.system('clear')
		print "Parsing news: " + str(int((i/float(len(paths)))*100)) + '%'

		news = {'path' : path, 'topic' : None, 'articles' : []}
		with open(path,'r') as f :
			for j  in [json.loads(line.strip()) for line in f if line.strip() != ''] :
				news['topic'] = j['topic']
				j.pop('topic')
				news['articles'].append(j)
		i += 1
		newJsons.append(news)
	
	os.system('clear')
	print "Parsing done: " + str(int((i/float(len(paths)))*100)) + '%'

	i = 0
	for j in newJsons :
		os.system('clear')
		print "Reformatting news: " + str(int((i/float(len(newJsons)))*100)) + '%'
		with open(j['path'],'w') as f :
			j.pop('path')
			f.write(json.dumps(j))
			i += 1
	os.system('clear')
	print "Reformatting done: " + str(int((i/float(len(newJsons)))*100)) + '%'
	print len(newJsons)

if __name__ == '__main__' :
	from sys import argv
	formatNews(argv[1])