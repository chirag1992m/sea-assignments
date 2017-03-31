#!/usr/bin/env python3

from itertools import groupby
from operator import itemgetter
import sys, pickle

data = []
while True:
	try:
		data.append(pickle.load(sys.stdin.buffer))
	except EOFError:
		break

for word, group in groupby(data, itemgetter(0)):
    total = sum(int(count) for _, count in group)
    pickle.dump((word, total), sys.stdout.buffer)
