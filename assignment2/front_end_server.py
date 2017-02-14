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
class FrontEndServer(web.RequestHandler):

	#GET request handler
	@gen.coroutine
	def get(self):
		queryString = self.get_query_argument("q", default="", strip=False)
		if not queryString:
			self.write("")
			return

		doc_priorities = yield self.__get_indexes(queryString=queryString)

		#Top 10 documents to be sent back
		topDocuments = self.__priority_sort_topk(indexes=doc_priorities)
		
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
		for indexServer in inventory.get_index_servers():
			try:
				response = yield http_client.fetch(indexServer + "?" + urllib.parse.urlencode(query))
				responseParsed = json.loads(str(response.body, 'utf-8'))
				
				if 'postings' in responseParsed:
					indexes.extend(responseParsed['postings'])

			except httpc.HTTPError as e:
				continue
			except Exception as e:
				continue

		http_client.close()
		return indexes

	def __priority_sort_topk(self, indexes, top_k=10):
		length = len(indexes)
		if length == 0:
			return []

		indexes.sort(key=lambda x:x[1], reverse=True) # Every entry is doc_id, tf_idf
		top_k = (top_k if top_k < length else length)

		doc_ids = []
		for doc_entry in indexes:
			doc_ids.append(doc_entry[0])

		return doc_ids[:top_k]

	@gen.coroutine
	def __get_doc_snippets(self, doc_ids, queryString):
		inventory = Inventory()

		snippets = []
		http_client = httpc.AsyncHTTPClient()

		numDocServers = inventory.get_num_doc_servers()
		docServers = inventory.get_doc_servers()
		for docId in doc_ids:
			try:
				serverId = (docId % numDocServers)

				query = {'id': docId, 'q': queryString}
				response = yield http_client.fetch(docServers[serverId] 
					+ "?" + urllib.parse.urlencode(query))

				responseParsed = json.loads(str(response.body, 'utf-8'))
				
				if 'results' in responseParsed:
					snippets.extend(responseParsed['results'])

			except httpc.HTTPError as e:
				continue
			except Exception as e:
				continue

		http_client.close()		
		return snippets

	def __pack_response(self, doc_snippets):
		result_dict = {"num_results": len(doc_snippets), 
						"results": doc_snippets}

		return json.dumps(result_dict, ensure_ascii=False)

# Main code to start the front-end server
if __name__ == "__main__":
	inventory = Inventory()

	app = web.Application([
		(r"/search", FrontEndServer)
	])
	port = inventory.get_port()

	app.listen(port)
	inventory.set_front_end(port)
	print("Front-End Server: ", port)

	inventory.add_index_server("http://linserv2.cims.nyu.edu:35315/index")
	inventory.add_index_server("http://linserv2.cims.nyu.edu:35316/index")
	inventory.add_index_server("http://linserv2.cims.nyu.edu:35317/index")

	inventory.add_doc_server("http://linserv2.cims.nyu.edu:35318/doc")
	inventory.add_doc_server("http://linserv2.cims.nyu.edu:35319/doc")
	inventory.add_doc_server("http://linserv2.cims.nyu.edu:35320/doc")
	
	iol.IOLoop.current().start()