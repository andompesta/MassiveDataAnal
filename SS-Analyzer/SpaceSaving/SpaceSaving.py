#!/usr/bin/python3

import collections
import hashlib

class SpaceSaving :
	def __init__ (self, size=10, stopWordFile="", HashSize=200) :
		self.k = size
		self.vals = []
		self.cnt = collections.Counter()
		self.hash_dim = HashSize
		try :
			with open(stopWordFile, 'r') as fin :
				self.stop_words = [line.strip('\n') for line in fin]
		except IOError :
			print("WARNING: no stop word file read (not needed, forgotten or wrong file name?)")
			self.stop_words = []

	# Check whether a word is a stop word and should be ignored
	def StopWord(self, word) :
		return word in self.stop_words

	def notify (self, word) :
		word = word.lower()
		if self.StopWord(word) :
			return
		# Update the hash table
		wordhash = int(hashlib.md5(word.encode("utf-8")).hexdigest(), 16) % self.hash_dim
		self.cnt[wordhash] += 1
		# If the word is already tracked, then update its number of occurrencies
		for v in self.vals :
			if v["word"] == word :
				v["occurrencies"] += 1
				return
		# Not track, but there is space to track it
		if len(self.vals) < self.k :
			self.vals.append({"word":word, "occurrencies":1, "error":0})
		# Check whether it should replace something else which is currently tracked
		else :
			occ = [x["occurrencies"] for x in self.vals]
			val, idx = min((val, idx) for (idx,val) in enumerate(occ))
			if self.cnt[wordhash] > val :
				self.vals[idx] = {"word":word, "occurrencies":self.vals[idx]["occurrencies"]+1, "error":self.vals[idx]["occurrencies"]}

	def print(self) :
		for v in self.vals :
			print("{0} \t\ttimes:{1} \t\terr:{2}".format(v["word"], v["occurrencies"], v["error"]))

	def smart_print(self, threshold) :
		for v in self.vals :
			if v["occurrencies"] - v["error"] >= threshold :
				print(v["word"])

