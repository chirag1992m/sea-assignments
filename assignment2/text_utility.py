# -*- coding: UTF-8 -*-
'''
Name: Chirag Maheshwari
Course: Search Engine Architecture

Text Based Utilities
'''
'''
'''

import nltk
import string

class StringCleaner:
	def __init__(self):
		self.__punctuations = set(string.punctuation)
		self.__stop_words = set(nltk.corpus.stopwords.words('english'))
		self.__stemmer = nltk.stem.snowball.SnowballStemmer("english")

	def __tokenize(self, query):
		return nltk.word_tokenize(query)

	def __remove_punctuations(self, wordVector):
		return [i.strip("".join(self.__punctuations)) for i in wordVector]

	def __remove_stop_words(self, wordVector):
		return [i for i in wordVector if i not in self.__stop_words]

	def __stem_word(self, wordVector):
		return [self.__stemmer.stem(i) for i in wordVector]

	def __clean_empty(self, wordVector):
		return [i for i in wordVector if i]

	def process_string(self, queryString):
		wordVector = self.__tokenize(queryString)
		stripPunctuations = self.__remove_punctuations(wordVector)
		stemmedWords = self.__stem_word(stripPunctuations)
		stripStopwords = self.__remove_stop_words(stemmedWords)

		return self.__clean_empty(stripStopwords)