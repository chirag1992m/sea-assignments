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
class FronEndServer(web.RequestHandler):

	#GET request handler
	@gen.coroutine
	def get(self):
		queryString = self.get_query_argument("q", default="", strip=False)
		if not queryString:
			self.write("")
			return

		indexes = yield self.__get_indexes(queryString)
		print(indexes)
		#topDocuments = self.__priority_sort_topk(indexes=indexes, top_k=10) #Top 10 documents to be sent back
		#docSnippets = yield self.__get_doc_snippets(doc_ids=topDocuments)

		#response = self.__pack_response(documents=docSnippets)
		response = queryString
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
				print("Am here!!")
				response = yield http_client.fetch(indexServer + "?" + urllib.parse.urlencode(query))
				print(str(response.body))
				responseParsed = {}
				
				if 'postings' in responseParsed:
					indexes.extend(responseParsed)

			except httpc.HTTPError as e:
				continue
			except Exception as e:
				continue

		return indexes

	def __priority_sort_topk(indexes, top_k=10):
		pass

	@gen.coroutine
	def __get_doc_snippets(doc_ids):
		pass

	def __pack_response(documents):
		pass

# Main code to start the front-end server
if __name__ == "__main__":
	inventory = Inventory()

	app = web.Application([
		(r"/search", FronEndServer)
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