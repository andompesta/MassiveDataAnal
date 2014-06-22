#!/usr/bin/python3

import json, argparse
from SpaceSaving.SpaceSaving import *

if __name__ == "__main__" :
	# Parsing arguments
	parser = argparse.ArgumentParser(description="Returns the most common words in a document")
	parser.add_argument("-f", help="Document to process", required=True, dest="input_file")
	parser.add_argument("-sw", help="Document containing words to be ignored", required=True, dest="sw_file")
	args = parser.parse_args()

	# Initializing the SpaceSaving classes
	ss = SpaceSaving(size=50, stopWordFile=args.sw_file)
	
	# Reading
	with open(args.input_file, 'r') as fin :
		for line in fin :
			news = json.loads(line.rstrip())
			main = news["headline"]["main"]
			lead = news["lead_paragraph"]
			full = news["full_text"]
			if isinstance(main, str) :
				for w in news["headline"]["main"].split() :
					ss.notify(w)
			if isinstance(lead, str) :
				for w in news["lead_paragraph"].split() :
					ss.notify(w)
			if isinstance(full, str) :
				for w in news["full_text"].split() :
					ss.notify(w)
	# Output
	ss.smart_print(3)

