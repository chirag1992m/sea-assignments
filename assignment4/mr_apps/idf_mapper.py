#!/usr/bin/env python3

import pickle, sys, hashlib
import xml.etree.ElementTree as et
import nltk
from collections import Counter

def get_doc_id(title):
	return (int(hashlib.md5(title.encode()).hexdigest()[:5], 16))

def get_text_vector(text):
	return nltk.word_tokenize(text)

def output_term_idf(page):
	title, text = "", ""
	for child in page.iter(None):
		if child.tag.endswith('title'):
			title = child.text

		if child.tag.endswith('text'):
			text = child.text

	doc_id = get_doc_id(title)
	words = get_text_vector(text)
	words.extend(get_text_vector(title))
	word_freq = Counter(words)

	for k, v in word_freq.items():
		pickle.dump((k, doc_id), sys.stdout.buffer)

while True:
	try:
		page = pickle.load(sys.stdin.buffer)
		output_term_idf(page)
	except EOFError:
		break
