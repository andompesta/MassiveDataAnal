from datetime import date

monthDict = {
	"January" : 1, \
	"February" : 2, \
	"March" : 3, \
	"April" : 4, \
	"May" : 5, \
	"June" : 6, \
	"July" : 7, \
	"August" : 8, \
	"September" : 9, \
	"October" : 10, \
	"November" : 11, \
	"December" : 12, \
}

class WikiParser :


	def __init__ (self, evFile, dFile) :
		self.elist = []
		try :
			with open(evFile, "r") as fin :
				for line in fin :
					self.readline(line)
			with open(dFile, "r") as fin :
				for line in fin :
					self.readline(line)
		except FileNotFoundError as exc :
			print("ERROR: Impossible to read wikipedia news files")
			raise exc

	def readline(self, line) :
		dateString = line.split(":")[0]
		monthString = dateString.split()[0]
		dayInt = int(dateString.split()[1])
		try : 
			pub_date = date(2009, monthDict[monthString], dayInt)
		except KeyError as exc :
			print("WARNING: problem encountered while parsing line", line)
			print("This line will be skipped")
			return
		content = line.split(":")[1]
		self.elist.append({"content":content, "pub_date":pub_date})

	def getNewsText(self) :
		return self.elist
