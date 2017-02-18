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

#To handle URLs and server responses and indexes
import pickle
import json

class IndexServer:
	
	'''
	Requests Handler Class
	'''
	class ServerHandler(web.RequestHandler):
		def initialize(self, database):
			self.__database = database

		#GET request handler
		@gen.coroutine
		def get(self):
			self.write(self.__database)

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

	index_base_file = "index_posting_"
	extension = ".index"
	for i in range(count):
		index_server = IndexServer(inventory.get_port(), index_base_file + str(i) + extension)
		index_server.start()
		index_servers.append(index_server)

	return index_servers

if __name__ == "__main__":
	index_servers = run_index_servers()
	iol.IOLoop.current().start()