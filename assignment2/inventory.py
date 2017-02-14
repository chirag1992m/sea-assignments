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
		self.__frontEnd = None
		
		self.__indexServers = []
		self.__numIndexServers = 0

		self.__documentServers = []
		self.__numDocumentServers = 0

		self.__port_generator = self.__generate_port()

	# Getter Functions
	def get_index_servers(self):
		return self.__indexServers

	def get_doc_Servers(self):
		return self.__documentServers

	def get_front_end(self):
		return self.__frontEnd

	def get_num_indexes(self):
		return self.__numIndexServers

	def get_doc_indexes(self):
		return self.__numDocumentServers

	# Check server authetication
	def __check_server(self, server):
		pass

	#Setter Functions
	def add_index_server(self, server):
		self.__check_server(server)
		self.__indexServers.append(server)
		self.__numIndexServers += 1

	def add_doc_server(self, server):
		self.__check_server(server)
		self.__documentServers.append(server)
		self.__numDocumentServers += 1

	def set_front_end(self, server):
		self.__check_server(server)
		self.__frontEnd = server

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