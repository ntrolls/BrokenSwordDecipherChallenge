import random
import levenshtein
import message
import wordlist
from operator import attrgetter

class submapping:
	def __init__(self, symbols, mapping=None, existing=None):
		self.symbols = list(symbols)
		if existing:
			self.existing = existing
		assigned = set(self.existing.keys())
		if mapping:
			self.mapping = dict(mapping)
		else:
			self.mapping = {}
			available = set(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']) - set(self.existing.values())
			for symbol in self.symbols:
				if symbol not in assigned:
					r = random.choice(list(available))
					self.mapping[symbol] = r
					available = available - set([r])
			# print 'mapping size:' + str(len(self.mapping)) + '/' + str(len(self.symbols))
			# print 'looking to map:' + str(self.mapping.keys())
	def __repr__(self):
		return str(self.mapping)
		
	def translate(self, coded_word):
		translated = ''
		m = dict(self.mapping)
		m.update(self.existing)
		for c in coded_word:
			translated = translated + m[c]
		return translated

class submapping_crossover:
	def crossover_onesided(self, parent_a, parent_b):
		assert(parent_a.symbols == parent_b.symbols)
		child = submapping(parent_a.symbols, parent_a.mapping, parent_a.existing)
		taken = set()
		for symbol in child.mapping.keys():
			if random.random() < 0.5:
				taken.add(child.mapping[symbol])
		for symbol in child.mapping.keys():
			if (child.mapping[symbol] not in taken and 
			    parent_a.mapping[symbol] != parent_b.mapping[symbol] and 
			    parent_b.mapping[symbol] not in taken):
				child.mapping[symbol] = parent_b.mapping[symbol]
		return child
	def crossover(self, parent_a, parent_b):
		return self.crossover_onesided(parent_a, parent_b), self.crossover_onesided(parent_b, parent_a)
		
class submapping_mutation:
	def mutate(self, original):
		mutated = submapping(original.symbols, original.mapping, original.existing)
		for symbol in mutated.mapping.keys():
			if random.random() < 0.3:
				available = set(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']) - set(mutated.existing.values())
				available = available - set(mutated.mapping.values())
				mutated.mapping[symbol] = random.choice(list(available))
		return mutated

class binarytournament:
	def select(self, population):
		i = random.randint(0, len(population) - 1)
		j = random.randint(0, len(population) - 1)
		while i == j:
		   j = random.randint(0, len(population) - 1)
		a = population[i]
		b = population[j]
		if a.fitness < b.fitness:
			return a
		else: 
			return b

class fitness:
	def __init__(self, coded_word, word_list):
		self.coded_word = coded_word
		self.word_list = word_list
	def measure(self, candidate_submapping):
		mapped = set(candidate_submapping.mapping.values())
		min_dist = len(self.coded_word)
		for word in self.word_list:
			dist, missed = levenshtein.lev_dist(candidate_submapping.translate(self.coded_word), word)
			if mapped.intersection(missed):
				dist = 100
			if dist < min_dist:
				min_dist = dist
		return min_dist

class ga:
	global message
	def __init__(self, partial_mapping, word_list):
		self.partial_mapping = partial_mapping
		self.word_list = word_list
	def evolve(self, coded_word):
		self.population = []
		self.selection_operator = binarytournament()
		self.crossover_operator = submapping_crossover()
		self.mutation_operator = submapping_mutation()
		self.fitness_function = fitness(coded_word, self.word_list)
		
		symbols = set(coded_word)
		pop_size = 30
		for i in range(pop_size):                      
			new_individual = submapping(symbols, {}, self.partial_mapping)
			new_individual.fitness = self.fitness_function.measure(new_individual)
			self.population.append(new_individual)

		generation = 0                             
		current_best = 100
		current_best_str = ''
		while generation < 50 and current_best > 0:
			self.nextgeneration = []
			self.nextgeneration.append(self.population[0])
			self.nextgeneration.append(self.population[pop_size - 1])
			while len(self.nextgeneration) < pop_size:
				parent_a = self.selection_operator.select(self.population)
				parent_b = self.selection_operator.select(self.population)
				child_a, child_b = self.crossover_operator.crossover(parent_a, parent_b)
				if random.random() < (2.0 / float(len(child_a.mapping))):
					child_a = self.mutation_operator.mutate(child_a)
					child_b = self.mutation_operator.mutate(child_b)
				child_a.fitness = self.fitness_function.measure(child_a)
				child_b.fitness = self.fitness_function.measure(child_b)
				self.nextgeneration.append(child_a)	
				self.nextgeneration.append(child_b)
				# print child_a
				# print child_b
			self.population = sorted(self.nextgeneration, key=attrgetter('fitness'))
			best = self.population[0]
			# print generation, best.fitness, best.translate(coded_word)
			if best.fitness < current_best:
				current_best = best.fitness
				current_best_str = best.translate(coded_word)
				# print current_best_str
			# print
			generation += 1
		if current_best == 0:
			return self.population[0].mapping
		else:
			return {}