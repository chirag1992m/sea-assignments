# -*- coding: UTF-8 -*-
'''
Name: Chirag Maheshwari
Course: Search Engine Architecture

Index Server,
Reads the database file from and loads it into memory
Starts an index server on a given port
On a query, gives top K document closest to the query
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

class IndexServer:
	
	'''
	Requests Handler Class
	'''
	class ServerHandler(web.RequestHandler):
		#GET request handler
		@gen.coroutine
		def get(self):
			pass

	def __load_index(self, index_file):
		return {}

	def __init__(self):
		self.__ports = []
		self.__indexes = []
		self.__apps = []

	def start_new_server(self, port, index_file):
		index = self.__load_index(index_file)

		#Start a new server
		app = web.Application([
			(r"/index", IndexServer.ServerHandler)
		])
		app.listen(port)

		print("Started Index Server on port: ", port)
		self.__ports.append(port)
		self.__apps.append(app)
		self.__indexes.append(index)

		inventory = Inventory()
		inventory.add_index_server(port)

def run_index_servers():
	inventory = Inventory()

	index_server = IndexServer()

	index_base_file = "index_posting_"
	extension = ".index"
	for i in range(3):
		index_server.start_new_server(inventory.get_port(), index_base_file + str(i) + extension)

if __name__ == "__main__":
	run_index_servers()

	iol.IOLoop.current().start()