'''
Name: Chirag Maheshwari
Course: Search Engine Architecture

Inventory Module
Task: Manages addresses of the Different Servers 
Involved in this Search Engine
'''

#To get a random open port
import hashlib
import getpass #Get current user info

'''
We want only one instance of the inventory class
and thus use the SingleTon Pattern
using the metaclass functionality
'''
class Singleton(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

'''
Inventory class
Singleton Object (Only one instance exist)
Constains the front end server,
list of index servers,
list of document servers
'''
class Inventory(metaclass=Singleton):
	def __init__(self):
		self._frontEnd = None
		self._indexServers = []
		self._documentServers = []

		self.__port_generator = self.__generate_port()

	# Getter Functions
	def get_index_servers(self):
		return self._indexServers

	def get_doc_Servers(self):
		return self._documentServers

	def get_front_end(self):
		return self._frontEnd

	#Check port authetication
	def __check_server(self, server):
		pass

	#Setter Functions
	def add_index_server(self, server):
		self.__check_server(server)
		self._indexServers.append(server)

	def add_doc_server(self, server):
		self.__check_server(server)
		self._documentServers.append(server)

	def set_front_end(self, server):
		self.__check_server(server)
		self._frontEnd = server

	'''
	Port Generator functionalities
	Uniquely generates and unused port to be used
	'''
	# Port Generator Core
	def __generate_port(self):
		MAX_PORT = 50000
		MIN_PORT = 10000
		BASE_PORT = int(hashlib.md5(getpass.getuser().encode()).hexdigest()[:8], 16) % \
			(MAX_PORT - MIN_PORT) + MIN_PORT

		index = 0
		while True:
			yield (BASE_PORT + index)
			index = index + 1

	# Port Generator interface
	def get_port(self):
		return next(self.__port_generator)


if __name__ == "__main__":
	inventory1 = Inventory()
	inventory1.add_index_server(1234)
	inventory1.add_index_server(1235)
	inventory1.add_doc_server(12)
	inventory1.set_front_end(345)

	print(inventory1.get_port())

	#Should contain the same values as
	#the class follows Singleton Pattern
	inventory2 = Inventory()
	print(inventory2.get_front_end())
	print(inventory2.get_index_servers())
	print(inventory2.get_doc_Servers())

	print(inventory1.get_port())
	print(inventory2.get_port())