import json
from datetime import date

class NewsParser :
	def __init__(self, publisher, newsFile, topic) :
		self.contentList = []
		try :
			with open(newsFile, "r") as fin :
				FileContent = json.loads(fin.readline().rstrip())
				t = FileContent["topic"]
				if t.lower() != topic.lower() :
					print("WARNING: the {0} news file may contain news on a different topic {1}".format(publisher, t))
				for news in FileContent["articles"] :
					headline = news["headline"]["main"] or ""
					lead_paragraph = news["lead_paragraph"] or ""
					full_text = news["full_text"] or ""
					content = headline + lead_paragraph + full_text
					date_tokens = news["pub_date"].split("T")[0].split("-")
					pub_date = date(int(date_tokens[0]), int(date_tokens[1]), int(date_tokens[2]))
					self.contentList.append({"content":content, "pub_date":pub_date})
		except FileNotFoundError as exc :
			print("ERROR: News file {0} seems to not exist".format(newsFile))
			raise exc

	def getNewsText(self) :
		return self.contentList
     
