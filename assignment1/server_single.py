#To get a random open port
import hashlib
import getpass #Get current user info

#Import tornado Libraries
import tornado.web as web
import tornado.ioloop as iol

#Class to handle incoming web requests
#Only handles the GET request
class MainHandler(web.RequestHandler):

	#GET request handler
	def get(self):
		#Simple Hello World application
		self.write("Hello World!")

#Generator to generate a port
#Uses current user hash to 
#choose a random base port
def GeneratePort():
	MAX_PORT = 50000
	MIN_PORT = 10000
	BASE_PORT = int(hashlib.md5(getpass.getuser().encode()).hexdigest()[:8], 16) % \
		(MAX_PORT - MIN_PORT) + MIN_PORT

	index = 0
	while True:
		yield (BASE_PORT + index)
		index = index + 1

#Main code to start the server
if __name__ == "__main__":
	app = web.Application([
		(r"/", MainHandler)
	])
	port = next(GeneratePort())
	print("Starting server on: ", port)
	app.listen(port)
	iol.IOLoop.current().start()
