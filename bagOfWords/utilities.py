import datetime

def readConfigFile(path) :
	with open(path,'r') as f :
		lines = [l for l in f if l != '' and l[0] != '#']
		params = map(lambda t : (t[0].strip(),t[-1].strip()), map(lambda l : l.partition('='),lines))
		return dict(params)

def unixTime(dt):
	dt = dt[:-1].partition('T')
	YYYY,MM,DD = map(int,dt[0].split('-'))
	hh,mm,ss = map(int,dt[-1].split(':'))
	epoch = datetime.datetime.utcfromtimestamp(0)
	delta = datetime.datetime(YYYY,MM,DD,hh,mm,ss) - epoch
	return int(delta.total_seconds())

def readableDatetime(timestamp):
	return str(datetime.datetime.utcfromtimestamp(timestamp)).replace(' ','T') + 'Z'
