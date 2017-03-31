# -*- coding: UTF-8 -*-
'''
Name: Chirag Maheshwari
Course: Search Engine Architecture

DocumentServer,
Loads the document store.
Starts a server on given port.
Given a query document and query, returns a
document snippet with highlighted query words.
'''
from assignment2.inventory import Inventory

#Import tornado Libraries
import tornado.web as web
import tornado.ioloop as iol
import tornado.gen as gen

#To handle URLs and server responses and indexes
import pickle
import json

import text_utility as tu

class DocumentServer:
	
	'''
	Requests Handler Class
	'''
	class ServerHandler(web.RequestHandler):
		def initialize(self, database):
			self.__database = database

		def __get_query(self):
			queryString = self.get_query_argument("q", default="", strip=False) 
			doc_id = int(self.get_query_argument("id", default=0, strip=False))

			return {'q': queryString, 'id': doc_id}

		def __pack_result(self, result):
			result_dict = {"results": [result]}
			return json.dumps(result_dict, ensure_ascii=False)

		def __write_result(self, result):
			self.write(self.__pack_result(result))

		def __error_result(self):
			return {"doc_id": "INVALID", "snippet": "", "title": "", "url": ""}

		def __bold_word(self, word):
			return "<strong>" + word + "</strong>"

		def __get_highlighted_text(self, text, query_vector):
			text_vector = text.split(" ")

			for idx, word in enumerate(text_vector):
				for query in query_vector:
					if word.lower() == query.lower():
						text_vector[idx] = self.__bold_word(word)

			return " ".join(text_vector)

		def __get_doc_snippet(self, doc_text, query_vector):
			text_vector = doc_text.split(" ")

			snippet = ""
			max_count = 3
			count = 0
			for idx, word in enumerate(text_vector):
				for query in query_vector:
					if word.lower() == query.lower():
						snippet = snippet + " ".join(text_vector[idx-11:idx+11]) + " ... "
						count += 1
						if count >= max_count:
							break

				if count >= max_count:
							break

			return self.__get_highlighted_text(snippet, query_vector)

		def __get_result(self, query):
			doc_id = query['id']
			if doc_id in self.__database:
				doc_info = self.__database[doc_id]
			else:
				return self.__error_result()

			query_words = tu.StringCleaner().process_string(query['q'])
			result = {
				'doc_id': doc_id,
				'snippet': self.__get_doc_snippet(doc_info[2], query_words),
				'url': doc_info[1],
				'title': self.__get_highlighted_text(doc_info[0], query_words)
			}

			return result

		#GET request handler
		@gen.coroutine
		def get(self):
			query_dict = self.__get_query()

			self.__write_result(self.__get_result(query_dict))


	def get_datastore(self):
		return self.__doc_store

	def __load_doc_store(self, doc_store_file):
		return pickle.load(open(doc_store_file, "rb"))

	def __init__(self, port, doc_store_file):
		self.__port = port
		self.__doc_store = self.__load_doc_store(doc_store_file)
		self.__app = None

	def start(self):
		if self.__app is None:
			#Start a new server
			app = web.Application([
				(r"/doc", DocumentServer.ServerHandler, dict(database=self.get_datastore()))
			])
			app.listen(self.__port)

			print("Started Document Server on port: ", self.__port)
			self.__app = app
			
			inventory = Inventory()
			inventory.add_doc_server(self.__port)

def run_document_servers(count=3):
	inventory = Inventory()

	document_servers = []

	document_base_file = "document_posting_"
	extension = ".index"
	for i in range(count):
		document_server = DocumentServer(inventory.get_port(), document_base_file + str(i) + extension)
		document_server.start()
		document_servers.append(document_server)

	return document_servers

if __name__ == "__main__":
	run_document_servers()

	iol.IOLoop.current().start()