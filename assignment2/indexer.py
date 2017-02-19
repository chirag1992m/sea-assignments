# -*- coding: UTF-8 -*-
'''
Name: Chirag Maheshwari
Course: Search Engine Architecture

Indexer,
A class that reads the dataset: "wiki_dataset.xml"
and outputs a pickled data for all the indexes constructed
'''
'''
'''
import pickle
import os.path as path

from math import log

import dataset_parser as dp

class Indexer:

	def __init__(self, indexServers, docServers, xmlFile):
		self.set_index_servers(indexServers, refresh=False)
		self.set_document_servers(docServers, refresh=False)
		self.set_dataset_file(xmlFile, refresh=False)

		self.__clean_indexes()
		self.__populate_indexes()

	def set_index_servers(self, indexServers, refresh=True):
		if not isinstance(indexServers, int):
			raise TypeError("number of index servers should be an integer")

		if indexServers < 0:
			raise ValueError("indexServers should be greater than zero")

		self.__numInvertedIndexes = indexServers
		self.__populate_indexes(refresh)

	def set_document_servers(self, docServers, refresh=True):
		if not isinstance(docServers, int):
			raise TypeError("number of index servers should be an integer")

		if docServers < 0:
			raise ValueError("docServer should be greater than zero")

		self.__numDocumentIndexes = docServers
		self.__populate_indexes(refresh)

	def set_dataset_file(self, xmlFile, refresh=True):
		if not isinstance(xmlFile, str):
			raise TypeError("XML filename is not a string")

		if not path.isfile(xmlFile):
			raise ValueError("XML File does not exist")

		self.__datasetFile = xmlFile
		self.__populate_indexes(refresh)

	def __clean_indexes(self):
		self.__inverted_indexes_partitioned = []
		for i in range(self.__numInvertedIndexes):
			self.__inverted_indexes_partitioned.append({})

		self.__document_store_partitioned = []
		for i in range(self.__numDocumentIndexes):
			self.__document_store_partitioned.append({})

		self.__numDocuments = 0

	def __add_document_to_index(self, doc_id, doc_info):
		bonus = 1 #TODO
		indexServer = (doc_id % self.__numInvertedIndexes)
		docServer = (doc_id % self.__numDocumentIndexes)

		self.__document_store_partitioned[docServer][doc_id] = \
				(doc_info['title'], doc_info['URL'], doc_info['text'])

		for word in doc_info['title_vector']:
			if word not in self.__inverted_indexes_partitioned[indexServer]:
				self.__inverted_indexes_partitioned[indexServer][word] = {}

			if doc_id not in self.__inverted_indexes_partitioned[indexServer][word]:
				self.__inverted_indexes_partitioned[indexServer][word][doc_id] = 0

			self.__inverted_indexes_partitioned[indexServer][word][doc_id] += 1 + bonus

		for word in doc_info['text_vector']:
			if word not in self.__inverted_indexes_partitioned[indexServer]:
				self.__inverted_indexes_partitioned[indexServer][word] = {}

			if doc_id not in self.__inverted_indexes_partitioned[indexServer][word]:
				self.__inverted_indexes_partitioned[indexServer][word][doc_id] = 0

			self.__inverted_indexes_partitioned[indexServer][word][doc_id] += 1

	def __get_word_global_count(self, word):
		count = 0
		for idx in range(len(self.__inverted_indexes_partitioned)):
			if word in self.__inverted_indexes_partitioned[idx]:
				count += len(self.__inverted_indexes_partitioned[idx][word].keys())
		return count

	def __calc_idf(self, word):
		idf = log(self.__numDocuments / float(self.__get_word_global_count(word)))
		if(idf < 0):
			print("Something wrong! Please check!")

		return idf

	def __make_tf_idf(self):
		for idx in range(len(self.__inverted_indexes_partitioned)):
			for word, inverted_index in self.__inverted_indexes_partitioned[idx].items():
				idf = self.__calc_idf(word)
				for doc_id in self.__inverted_indexes_partitioned[idx][word]:
					self.__inverted_indexes_partitioned[idx][word][doc_id] *= idf

	def __populate_indexes(self, refresh=True):
		if not refresh:
			return

		parser = dp.DatasetParser(self.__datasetFile)

		for docParsed in parser.parsed_documents_iterator():
			self.__numDocuments += 1
			self.__add_document_to_index(self.__numDocuments, docParsed)

		self.__make_tf_idf()
		

	def write_index_to_file(self):
		baseIndexFile = "index_posting_"
		baseDocumentFile = "document_posting_"

		extension = ".index"

		for idx, indexes in enumerate(self.__inverted_indexes_partitioned):
			pickle.dump(indexes, open(baseIndexFile + str(idx) + extension, "wb"), protocol=3)

		for idx, docStore in enumerate(self.__document_store_partitioned):
			pickle.dump(docStore, open(baseDocumentFile + str(idx) + extension, "wb"), protocol=3)

def run_indexer():
	indexer = Indexer(3, 3, "wiki_dataset.xml")
	indexer.write_index_to_file()

if __name__ == "__main__":
	run_indexer()