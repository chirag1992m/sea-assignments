'''
Name: Chirag Maheshwari
Course: Search Engine Architecture

Front-End Server
'''
from inventory import Inventory

#Import tornado Libraries
import tornado.web as web
import tornado.ioloop as iol

# Class to handle incoming web requests
# Only handles the GET request
class FronEndServer(web.RequestHandler):

	#GET request handler
	def get(self):
		self.write(self.get_query_argument("q", strip=True))

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
	
	iol.IOLoop.current().start()