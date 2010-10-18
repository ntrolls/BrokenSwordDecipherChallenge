import submapping
import wordlist
import message
import levenshtein

word_list = wordlist.wordlist()
coded_message = message.message()
solution = {}

ordered_message = coded_message.getorderedcodedwords()

for coded_word in ordered_message:
	coded_word_len = len(coded_word)
	
	known = set(solution.keys())
	unknown = set(coded_word)
	if len(unknown - known) == 0:
		print
		print "coded word already known: " + str(coded_word) + " -> " + coded_message.decodeword(coded_word, solution)
		continue
	
	filtered_word_list = word_list.getfilteredlist(coded_word)
	if len(filtered_word_list) == 1:
		partial_mapping = word_list.convertmatchtomapping(coded_word, filtered_word_list[0])
		print filtered_word_list[0]
		newly_known = set(partial_mapping.keys()) - set(solution.keys())
		for key in newly_known:
			if partial_mapping[key] not in set(solution.values()):
				solution[key] = partial_mapping[key]                  	
	else:
		solver = submapping.ga(solution, filtered_word_list)
		print "invoking GA"
		solution.update(solver.evolve(coded_word))
	print "################################################"
	print str(coded_word) + "->" + coded_message.decodeword(coded_word, solution)
	print "################################################"
	print solution
	print "################################################"
	print coded_message.decode(solution)
	print "################################################"
	
	coded_message.updateknown(solution)

	if len(solution) == 26:
		break 
	else:
		print "size of current mapping:" + str(len(solution))
print coded_message.decode(solution)