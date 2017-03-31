#!/usr/bin/env python3

import pickle, sys
from itertools import groupby
from operator import itemgetter

data = []
while True:
	try:
		data.append(pickle.load(sys.stdin.buffer))
	except EOFError:
		break

inv_index = {}
for doc, term_freq in data:
	term, count = term_freq
	if term not in inv_index:
		inv_index[term] = {}
	inv_index[term][doc] = count

pickle.dump(inv_index, sys.stdout.buffer)