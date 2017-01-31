#To get a random open port
import hashlib
import getpass #Get current user info

#Import tornado Libraries
import tornado.web as web
import tornado.ioloop as iol
import tornado.gen as gen
import tornado.httpclient as httpc

def RoundRobinPortGenerator():
	start = 11943
	end = 11945
	diff = end - start + 1

	index = 0
	while True:
		yield start + index
		index = (index + 1) % diff

#Class to handle incoming web requests
#Only handles the GET request
class MainHandler(web.RequestHandler):
	portGenerator = RoundRobinPortGenerator()

	#GET request handler
	@tornado.gen.coroutine
	def get(self):
		#Simple Hello World application
		http_client = httpc.AsyncHTTPClient()
		try:
			response = yield http_client.fetch("http://linserv1.cims.nyu.edu:" + str(next(MainHandler.portGenerator)) + "/")
			self.write(response.body)
		except httpc.HTTPError as e:
			self.write("HTTP Error: " + str(e))
		except Exception as e:
			self.write("Server Error: " + str(e))
		http_client.close()

#Main code to start the server
if __name__ == "__main__":
	app = web.Application([
		(r"/", MainHandler)
	])
	port = 11940
	print("Starting FrontEnd on: ", port)
	app.listen(port)
	
	iol.IOLoop.current().start()
