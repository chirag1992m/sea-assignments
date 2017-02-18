# -*- coding: UTF-8 -*-
'''
Name: Chirag Maheshwari
Course: Search Engine Architecture

Front-End Server
'''
from inventory import Inventory

#Import tornado Libraries
import tornado.web as web
import tornado.ioloop as iol
import tornado.gen as gen
import tornado.httpclient as httpc

#To handle URLs and server responses
import urllib
import json

# Class to handle incoming web requests
# Only handles the GET request
class FrontEndServer:
	_hostname = None

	'''
	Internal Requests Handler class
	'''
	class ServerHandler(web.RequestHandler):
		def initialize(self):
			if FrontEndServer._hostname is None:
				index = self.request.host.index(':')
				FrontEndServer._hostname = "http://" + self.request.host[:index+1]

		#GET request handler
		@gen.coroutine
		def get(self):
			queryString = self.get_query_argument("q", default="", strip=False)
			if not queryString:
				self.write("")
				return

			docPriorities = yield self.__get_indexes(queryString=queryString)
			
			#Top 10 documents to be sent back
			topDocuments = self.__get_topk(indexes=docPriorities)
			
			#Get the document snippets for these documents
			docSnippets = yield self.__get_doc_snippets(doc_ids=topDocuments, queryString=queryString)
			
			response = self.__pack_response(doc_snippets=docSnippets)
			
			# Finally Write the response
			self.write(response)

		@gen.coroutine
		def __get_indexes(self, queryString=""):
			inventory = Inventory()

			query = {'q': queryString}

			indexes = []

			http_client = httpc.AsyncHTTPClient()
			responses = yield [http_client.fetch(FrontEndServer._hostname + str(indexServer) + "/index?" \
												+ urllib.parse.urlencode(query), 
												raise_error=False) \
								for indexServer in inventory.get_index_servers()]
			http_client.close()

			for response in responses:
				try:
					response.rethrow()
					responseParsed = json.loads(str(response.body, 'utf-8'))

					if 'postings' in responseParsed:
						indexes = self.__merge_indexes(indexes, responseParsed['postings'])

				except Exception as e:
					print(e)
					continue

			return indexes

		def __merge_indexes(self, a, b):
			merged = []

			while a and b:
				if a[0][1] > b[0][1]:
					merged.append(a.pop(0))
				else:
					merged.append(b.pop(0))

			return merged + a + b

		def __get_topk(self, indexes, k=10):
			doc_ids = []
			for doc_entry in indexes[:k]:
				doc_ids.append(doc_entry[0])

			return doc_ids

		@gen.coroutine
		def __get_doc_snippets(self, doc_ids, queryString):
			inventory = Inventory()

			snippets = []
			http_client = httpc.AsyncHTTPClient()

			numDocServers = inventory.get_num_doc_servers()
			docServers = inventory.get_doc_servers()

			urls = []
			for docId in doc_ids:
				serverId = (docId % numDocServers)

				query = {'id': docId, 'q': queryString}
				urls.append(FrontEndServer._hostname + str(docServers[serverId]) + \
							"/doc?" + urllib.parse.urlencode(query))

			responses = yield [http_client.fetch(url, raise_error=False) for url in urls]

			for response in responses:
				try:
					response.rethrow()

					responseParsed = json.loads(str(response.body, 'utf-8'))
					if 'results' in responseParsed:
						snippets.extend(responseParsed['results'])

				except Exception as e:
					print(e)
					continue

			http_client.close()
			return snippets

		def __pack_response(self, doc_snippets):
			result_dict = {"num_results": len(doc_snippets), 
							"results": doc_snippets}

			return json.dumps(result_dict, ensure_ascii=False)

	'''
	Server Functions
	'''
	def __init__(self, port):
		self.__port = port
		self.__app = None

	def start(self):
		if self.__app is None:
			self.__app = web.Application([
				(r"/search", FrontEndServer.ServerHandler)
			])

			self.__app.listen(self.__port)

			print("Started Front-End Server on port: ", self.__port)

			inventory = Inventory()
			inventory.set_front_end(self.__port)

def run_front_end():
	inventory = Inventory()
	front_end_server = FrontEndServer(inventory.get_port())
	front_end_server.start()

	return front_end_server

# Main code to start the front-end server
if __name__ == "__main__":
	run_front_end()

	inventory = Inventory()
	inventory.add_index_server("http://linserv2.cims.nyu.edu:35315/index")
	inventory.add_index_server("http://linserv2.cims.nyu.edu:35316/index")
	inventory.add_index_server("http://linserv2.cims.nyu.edu:35317/index")

	inventory.add_doc_server("http://linserv2.cims.nyu.edu:35318/doc")
	inventory.add_doc_server("http://linserv2.cims.nyu.edu:35319/doc")
	inventory.add_doc_server("http://linserv2.cims.nyu.edu:35320/doc")
	
	iol.IOLoop.current().start()