'''
Name: Chirag Maheshwari
Course: Search Engine Architecture

Inventory Module
Task: Manages addresses of the Different Servers 
Involved in this Search Engine
'''

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

	# Getter Functions
	def get_index_servers(self):
		return self._indexServers

	def get_doc_Servers(self):
		return self._documentServers

	def get_front_end(self):
		return self._frontEnd

	#Check port authetication
	def _check_server(self, server):
		pass

	#Setter Functions
	def add_index_server(self, server):
		self._check_server(server)
		self._indexServers.append(server)

	def add_doc_server(self, server):
		self._check_server(server)
		self._documentServers.append(server)

	def set_front_end(self, server):
		self._check_server(server)
		self._frontEnd = server


if __name__ == "__main__":
	inventory1 = Inventory()
	inventory1.add_index_server(1234)
	inventory1.add_index_server(1235)
	inventory1.add_doc_server(12)
	inventory1.set_front_end(345)

	#Should contain the same values as
	#the class follows Singleton Pattern
	inventory2 = Inventory()
	print(inventory2.get_front_end())
	print(inventory2.get_index_servers())
	print(inventory2.get_doc_Servers())