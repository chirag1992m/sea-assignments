#!/usr/bin/env python3

import sys, nltk
import pickle

for line in sys.stdin:
	for word in nltk.word_tokenize(line.strip()):
		pickle.dump((word, 1), sys.stdout.buffer)
