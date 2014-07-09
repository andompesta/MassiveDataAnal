#!/usr/bin/python3

import collections

class SpaceSaving :
	def __init__ (self, k_=10, swf="", hd=200) :
		self.k = k_
		self.vals = []
		self.cnt = collections.Counter()
		self.hash_dim = hd
		try :
			with open(swf, 'r') as fin :
				self.stop_words = [line.strip('\n') for line in fin]
		except IOError :
			print("WARNING: no stop word file read (not needed, forgotten or wrong file name?)")
			self.stop_words = []

	def StopWord(self, word) :
		return word in self.stop_words

	def notify (self, word) :
		word = word.lower()
		if self.StopWord(word) :
			return

		h = hash(word) % self.hash_dim
		self.cnt[h] += 1
		
		for v in self.vals :
			if v["word"] == word :
				v["occurrencies"] += 1
				return
					
		if len(self.vals) < self.k :
			self.vals.append({"word":word, "occurrencies":1, "error":0})
		else :
			occ = [x["occurrencies"] for x in self.vals]
			val, idx = min((val, idx) for (idx,val) in enumerate(occ))
			if self.cnt[h] > val :
				self.vals[idx] = {"word":word, "occurrencies":self.vals[idx]["occurrencies"]+1, "error":self.vals[idx]["occurrencies"]}

	def print(self) :
		for v in self.vals :
			print("{0} \t\ttimes:{1} \t\terr:{2}".format(v["word"], v["occurrencies"], v["error"]))

	def smart_print(self, threshold) :
		for v in self.vals :
			if v["occurrencies"] - v["error"] >= threshold :
				print(v["word"])

