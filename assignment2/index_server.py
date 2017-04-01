# -*- coding: UTF-8 -*-
'''
Name: Chirag Maheshwari
Course: Search Engine Architecture

Index Server,
Reads the database file from and loads it into memory
Starts an index server on a given port
On a query, gives top K document closest to the query
'''
from assignment2.inventory import Inventory

#Import tornado Libraries
import tornado.web as web
import tornado.ioloop as iol
import tornado.gen as gen

#To handle URLs and server responses and indexes
import pickle
import json

from assignment2 import text_utility as tu

class IndexServer:
	
	'''
	Requests Handler Class
	'''
	class ServerHandler(web.RequestHandler):
		def initialize(self, database):
			self.__database = database

		def __get_query(self):
			return self.get_query_argument("q", default="", strip=False)

		def __pack_result(self, results):
			result_dict = {"postings": results}
			return json.dumps(result_dict, ensure_ascii=False)

		def __write_result(self, results):
			self.write(self.__pack_result(results))

		def __closest_results(self, scores, k=10):
			closest_results = []
			for doc, score in scores.items():
				if score > 0:
					closest_results.append((doc, score))

			closest_results.sort(key=lambda x:x[1], reverse=True)

			return closest_results[:k]


		def __get_doc_scores(self, query_vector):
			scores = {}
			query_count = {}

			for word in query_vector:
				if word in query_count:
					query_count[word] += 1
				else:
					query_count[word] = 1

			for word, count in query_count.items():
				if word in self.__database:
					for doc, doc_count in self.__database[word].items():
						score = count * doc_count
						if doc in scores:
							scores[doc] += score
						else:
							scores[doc] = score
			return scores

		def __get_results(self, query):
			#Writing an empty result if no query is provided
			if not query:
				return []

			queryVector = tu.StringCleaner().process_string(query)
			scores = self.__get_doc_scores(queryVector)

			return self.__closest_results(scores)

		#GET request handler
		@gen.coroutine
		def get(self):
			queryString = self.__get_query()

			self.__write_result(self.__get_results(queryString))


	def get_index(self):
		return self.__index

	def __load_index(self, index_file):
		return pickle.load(open(index_file, "rb"))

	def __init__(self, port, index_file):
		self.__port = port
		self.__index = self.__load_index(index_file)
		self.__app = None

	def start(self):
		if self.__app is None:
			#Start a new server
			app = web.Application([
				(r"/index", IndexServer.ServerHandler, dict(database=self.get_index()))
			])
			app.listen(self.__port)

			print("Started Index Server on port: ", self.__port)
			self.__apps = app

			inventory = Inventory()
			inventory.add_index_server(self.__port)

def run_index_servers(count=3):
	inventory = Inventory()

	index_servers = []

	index_base_file = "assignment2/index_posting_"
	extension = ".index"
	for i in range(count):
		index_server = IndexServer(inventory.get_port(), index_base_file + str(i) + extension)
		index_server.start()
		index_servers.append(index_server)

	return index_servers

if __name__ == "__main__":
	index_servers = run_index_servers()
	iol.IOLoop.current().start()