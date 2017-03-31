#!/usr/bin/env python3

import pickle, sys

doc_store = {}
while True:
	try:
		data = pickle.load(sys.stdin.buffer)
		doc_store[data[0]] = data[1]
	except EOFError:
		break

pickle.dump(doc_store, sys.stdout.buffer)
