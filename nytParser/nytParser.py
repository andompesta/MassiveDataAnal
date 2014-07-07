from bs4 import BeautifulSoup


def parseNews(url,opener) :
	
	fulltext = ''
	soup = BeautifulSoup(opener.open(url))

	if soup.find('nyt_text') != None :
		for div in soup.find('nyt_text').findAll('div') : div.extract()
		for paragraph in soup.find('nyt_text').findAll('p') : fulltext = fulltext + '\n' + paragraph.text.strip()
	
	elif soup.find('div',attrs={'class':'articleBody'}) != None :
		for paragraph in soup.findAll('p',attrs={'itemprop':'articleBody'}) : fulltext = fulltext + '\n' + paragraph.text.strip()
	elif soup.find('p',attrs={'class':'story-body-text'}) != None :
		for paragraph in soup.findAll('p',attrs={'class':'story-body-text'}) : fulltext = fulltext + '\n' + paragraph.text.strip()
	else :
		raise Exception("nytParser: bad schema!")

	# more pages?
	if soup.find('a', attrs={'class':'next'}) != None :
		fulltext += parseNews('query.nytimes.com'+soup.find('a', attrs={'class':'next'})['href'],opener)

	return fulltext


def test(html) :

	fulltext = ''
	soup = BeautifulSoup(html)

	if soup.find('nyt_text') != None :
		for div in soup.find('nyt_text').findAll('div') : div.extract()
		for paragraph in soup.find('nyt_text').findAll('p') : fulltext += paragraph.text
	
	elif soup.find('div',attrs={'class':'articleBody'}) != None :
		for paragraph in soup.findAll('p',attrs={'itemprop':'articleBody'}) : fulltext += paragraph.text.strip()
	elif soup.find('p',attrs={'class':'story-body-text'}) != None :
		for paragraph in soup.findAll('p',attrs={'class':'story-body-text'}) : fulltext += paragraph.text.strip()
	else :
		raise Exception("nytParser: bad schema!")

	return fulltext

