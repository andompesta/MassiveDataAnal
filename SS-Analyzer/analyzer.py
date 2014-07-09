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
	ss = SpaceSaving(k_=30, swf=args.sw_file)
	
	# Reading
	with open(args.input_file, 'r') as fin :
		for line in fin :
			news = json.loads(line.rstrip())
			[ss.notify(w) for w in news["headline"]["main"].split()]
			[ss.notify(w) for w in news["lead_paragraph"].split()]

	# Output
	ss.smart_print(3)

