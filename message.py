class message:

	def __init__(self):
		self.message = [[4,22,0,12,12,0],[16,8,25,25],[12,0,4,3,12,19],[19,3],[16,3,25,25,3,20],[5,8,19],[19,18,22,13],[22,13],[19,3,3],[8,12,17,0,21,19],[19,3],[20,6,22,19],[6,12,21,3],[6,21,10],[14,6,1,6,10,6],[5,3,19,18],[10,0,6,10],[19,18,22,13],[22,13],[21,3,19],[6],[7,3,22,21,7,22,10,0,21,7,0],[22,21,10,0,0,10],[22,19],[13,0,0,1,13],[19,18,6,19],[6,25,25],[3,16],[8,13],[20,18,3],[7,6,1,0],[19,3,17,0,19,18,0,12],[22,21],[2,8,25,14],[6,12,0],[22,21],[10,6,21,17,0,12],[19,6,24,0],[17,12,0,6,19],[7,6,12,0],[23]]
		self.assigned_codes = {}

	def getorderedcodedwords(self):
		# return sorted(self.message, key=lambda x:len(x), reverse=True)
		# return sorted(self.message, key=lambda x:len(x) + len(set(x) - set(self.assigned_codes.keys())), reverse=True)
		return sorted(self.message, key=lambda x:len(x) + len(set(x).intersection(set(self.assigned_codes.keys()))), reverse=True)
		# return sorted(self.message, key=lambda x:len(x) + len(set(x).intersection(set(self.assigned_codes.keys()))))

	def decodeword(self, coded_word, mapping):
		c = ''
		for code in coded_word:
			if mapping.has_key(code):
				c = c + mapping[code]
			else:
				c = c + '*'
		return c
			
	def decode(self, mapping):
		s = ''
		for m in self.message:
			s = s + self.decodeword(m, mapping) + ' '
		return s
		
	def updateknown(self, known):
		self.assigned_codes.update(known)