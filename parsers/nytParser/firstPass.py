import urllib2
import urllib
import json
from cookielib import CookieJar
from sys import argv
import os
import nytParser

def read_credentials(path) :
	with open(path) as f :
		return f.read().strip().split('\n')[:2]


# type-of-material blacklist
tom_blacklist = ['Summary','Schedule','Video','Paid Death Notice','Interactive Feature','List','Slideshow']

if __name__ == '__main__' :

	if len(argv) != 5 :
		print '''USAGE: python firstPass.py ARGS
		ARGS:
		\tcredential file
		\told json folder
		\tnew json folder
		\tlog file path
		'''

	else :

		# read credentials file
		userid,password = read_credentials(argv[1])

		# read all the json paths
		json_paths = map(lambda f: argv[2]+f, os.listdir(argv[2]))

		output_path = argv[3]
		log_path = argv[4]

		#Enable cookies
		cj = CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		login_data = urllib.urlencode({'userid' : userid, 'password' : password})
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		opener.open('https://myaccount.nytimes.com/auth/login', login_data)

		

		ok,fail = 0,0

		f_log = open(log_path,'w')

		for path in json_paths :
			
			f = open(path)
			article_list = [json.loads(line) for line in f.read().strip().split('\n')]
			f.close()
			
			articles = {}
			new_jsons = []
			topic = path.partition('.')[0].partition('-')[-1]

			f_ok_out = open(output_path + 'ok_' + topic + '.json','w')
			f_fail_out = open(output_path + 'fail_' + topic + '.json','w')
			
			# scans every article in the current json, except those with a blacklisted 'type_of_material'
			
			articles_processed = 0
			for article in article_list :

				print str(articles_processed) + '/' + str(len(article_list)) + '\t[' + topic + ']\tOK/FAIL: ' + str(ok) + '/' + str(fail)
				articles_processed += 1

				if (not 'type_of_material' in article) or article['type_of_material'] not in tom_blacklist :
					if 'topic' not in article :
						article['topic'] = topic   # stores also the topic inside the json
					
					if 'full_text' not in article :
						if article['web_url'] in articles : 
							# already got that in this session
							article['full_text'] = articles[article['web_url']]
							ok += 1
						else : # parse the article
							try :
								text = nytParser.parseNews(article['web_url'],opener)
							except Exception as e :
								f_log.write(str(article['_id']['$oid']) + '\t' + str(article['topic']) + '\t' + str(article['web_url']) + '\t' + str(e.message) + '\n')
								text = ''
								
							if text != '' :
								articles[article['web_url']] = text
								article['full_text'] = text
								ok += 1
							else :
								fail += 1

					new_jsons.append(article)

			for j in new_jsons :
				if 'full_text' in j : f_ok_out.write(json.dumps(j)+'\n')
				else : f_fail_out.write(json.dumps(j)+'\n')
			

			f_ok_out.close()
			f_fail_out.close()
										
		f_log.close()

		print 'TOTAL: ok: ' + str(ok)
		print 'TOTAL: fail: ' + str(fail)
