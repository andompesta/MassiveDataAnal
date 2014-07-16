#!/usr/bin/python3

import collections
import hashlib

class SpaceSaving :
	def __init__ (self, size=10, stopWordsList=[], HashSize=1000) :
		self.k = size
		self.vals = []
		self.cnt = collections.Counter()
		self.hash_dim = HashSize
		self.stopWords = stopWordsList

	# Check whether a word is a stop word and should be ignored
	def StopWord(self, word) :
		return word in self.stopWords

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

	def getSmartList(self, threshold=3) :
		wlist = []
		for v in self.vals :
			value = v["occurrencies"] - v ["error"]
			if value >= threshold :
				wlist.append({"word":v["word"], "value":value})
		return wlist

	def getBestWords(self, n = None) :
		if n == None : n = len(self.vals)
		smartList = [{"word":v["word"], "value":v["occurrencies"]-v["error"]} for v in self.vals]
		smartList.sort(key=(lambda d: d["value"]), reverse=True)
		return smartList[:n]



