#!/usr/bin/env python3

import pickle, sys, hashlib
import xml.etree.ElementTree as et

def get_doc_id(title):
	return (int(hashlib.md5(title.encode()).hexdigest()[:5], 16))

def get_url(title):
	return "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")

def output_doc_term_freq(page):
	title, text, url = "", "", ""
	for child in page.iter(None):
		if child.tag.endswith('title'):
			title = child.text

		if child.tag.endswith('text'):
			text = child.text

	url = get_url(title)
	doc_id = get_doc_id(title)

	pickle.dump((doc_id, (title, url, text)), sys.stdout.buffer)

while True:
	try:
		page = pickle.load(sys.stdin.buffer)
		output_doc_store(page)
	except EOFError:
		break
