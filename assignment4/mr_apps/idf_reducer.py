#!/usr/bin/env python3

import pickle, sys
import math

idf = {}
doc_ids = []
while True:
	try:
		word, doc = pickle.load(sys.stdin.buffer)
		if word not in idf:
			idf[word] = 0
		idf[word] += 1
		doc_ids.append(doc)
	except EOFError:
		break

num_docs = float(len(set(doc_ids)))
for k in idf.keys():
	idf[k] = math.log(num_docs/idf[k])

pickle.dump(idf, sys.stdout.buffer)
