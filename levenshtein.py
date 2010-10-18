def generic_lev_dist(s, t):
	m = len(s)
	n = len(t)
	
	d = numpy.zeros((m + 1, n + 1), dtype=int)
	for i in range(0, m + 1):
		d[i, 0] = i
	for j in range(0, n + 1):
		d[0, j] = j
		
	for j in range(1, n):
		for i in range(1, m):
			if s[i] == t[j]:
				d[i, j] = d[i - 1, j - 1]
			else:
				d[i, j] = int(min([d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + 1]))
	return d[m-1, n-1]

def lev_dist(s, t):
	# we only compare words of same length, so there is only change operation
	count = 0
	missed = set()
	for i in range(len(s)):
		if s[i] != t[i]:
			count = count + 1
			missed.add(t[i])
	return count, missed