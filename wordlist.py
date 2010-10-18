import os
import pickle
import message

class wordlist:

	def __init__(self):
		if os.path.exists('words_table.dat'):
			self.word_table = pickle.load(file('words_table.dat'))
		else:
			self.word_table = {}
			words = open('2of12inf.txt', 'r').readlines()
			for word in words:
				word = word.strip()
				l = len(word)
				if self.word_table.has_key(l):
					self.word_table[l].append(word)
				else:
					self.word_table[l] = [word]
			pickle.dump(self.word_table, open('./words_table.dat', 'w'))   

	def extractpattern(self, word):
		seen = {}
		pattern = []
		for c in word:
			if seen.has_key(c):
				pattern.append(seen[c])
			else:
				next_pk = len(seen)
				seen[c] = next_pk
				pattern.append(next_pk)
		return pattern

	def getfilteredlist(self, coded_word):
		print
		print "filtering for " + str(coded_word) + "."
		unfiltered = self.word_table[len(coded_word)]
		print "unfiltered:" + str(len(unfiltered))
		filtered = []
		code_pattern = self.extractpattern(coded_word)
		for word in unfiltered:
			if self.extractpattern(word) == code_pattern:
				filtered.append(word)
		print "filtered:" + str(len(filtered))
		return filtered
		
	def convertmatchtomapping(self, coded_word, word):
		mapping = {}
		for i in range(len(coded_word)):
			mapping[coded_word[i]] = word[i]
		return mapping