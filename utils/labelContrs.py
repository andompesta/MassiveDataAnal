#!/usr/bin/python3

import json, configparser, argparse, random, sys

if __name__ == "__main__" :
	parser = argparse.ArgumentParser(description="Extract tweets of given topic and contradiction point")
	parser.add_argument("-t", help="topic", required=True, dest="topic")
	parser.add_argument("-c", help="contradiction point (starting from 1)", required=True, dest="point", type=int)
	parser.add_argument("-n", help="number of tweets to display at a time", required=False, default=10, dest="shown", type=int)
	args = parser.parse_args()
	config = configparser.RawConfigParser()
	config.read("config.ini")

	contrFile = config["Paths"]["ContrFile"].replace("XXX", args.topic)
	tweetsFile = config["Paths"]["TweetFile"].replace("XXX", args.topic)
	
	# Check whether a label already exists
	contrs = json.load(open(contrFile,'r'))
	try :
		prev_label = contrs["contradictions"][args.point - 1]["label"]
		if prev_label != None :
			ans = input("WARNING: this point has already been marked as {0}. Want to continue? (y/N) ".format(prev_label))
			if ans != "y": sys.exit(0)
	except KeyError:
		pass

	with open(tweetsFile, 'r') as fin :
		tweets = json.loads(fin.readlines()[args.point - 1])
		while True :
			sample = random.sample(tweets, args.shown)
			for s in sample : print(s["text"])
			label = input("Insert the label for this contradiction or an empty line: ")
			print()
			if label != "" : break
	
	# Writing the label on the contradiction file
	contrs["contradictions"][args.point - 1]["label"] = label
	json.dump(contrs, open(contrFile, 'w'))



