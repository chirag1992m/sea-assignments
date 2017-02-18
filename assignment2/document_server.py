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
from inventory import Inventory

#Import tornado Libraries
import tornado.web as web
import tornado.ioloop as iol
import tornado.gen as gen
import tornado.httpclient as httpc

#To handle URLs and server responses and indexes
import pickle
import json

class DocumentServer:
	
	'''
	Requests Handler Class
	'''
	class ServerHandler(web.RequestHandler):
		#GET request handler
		@gen.coroutine
		def get(self):
			pass

	def __load_doc_store(self, doc_store_file):
		return {}

	def __init__(self):
		self.__ports = []
		self.__doc_stores = []
		self.__app = []

	def start_new_server(self, port, doc_store_file):
		index = self.__load_doc_store(doc_store_file)

		#Start a new server
		app = web.Application([
			(r"/doc", DocumentServer.ServerHandler)
		])
		app.listen(port)

		print("Started Document Server on port: ", port)
		self.__port.append(port)
		self.__app.append(app)

		inventory = Inventory()
		inventory.add_doc_server(port)

def run_document_servers():
	inventory = Inventory()

	document_server = DocumentServer()

	document_base_file = "document_posting_"
	extension = ".index"
	for i in range(3):
		document_server.start_new_server(inventory.get_port(), document_base_file + str(i) + extension)

if __name__ == "__main__":
	run_index_servers()