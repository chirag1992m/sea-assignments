#Assignment - 1 Script
#Name: Chirag Maheshwari
#Course: Search Engine Architecture

#Imports for randopm port generation
import hashlib
import getpass #Get current user info

#Import tornado Libraries
import tornado.web as web
import tornado.ioloop as iol
import tornado.httpserver as https
import tornado.gen as gen
import tornado.httpclient as httpc
import tornado.process as proc

#Class to handle incoming web requests
#Only handles the GET request
class BackendHandler(web.RequestHandler):

	#GET request handler
	def get(self):
		#Simple Hello World application
		self.write(self.request.host)

#Generator to generate a port
#Uses current user hash to
#choose a random base port
def GetBasePort():
	MAX_PORT = 50000
	MIN_PORT = 10000
	BASE_PORT = int(hashlib.md5(getpass.getuser().encode()).hexdigest()[:8], 16) % \
		(MAX_PORT - MIN_PORT) + MIN_PORT

	return BASE_PORT


#Start the Backend Servers
serverApp = web.Application([
	(r"/", BackendHandler)
])

basePort = GetBasePort()

pid = proc.fork_processes(4, max_restarts=1) #1-Frontend and 3-Backend

if pid != 0: #Not the main process where the frontend server will run
	server = https.HTTPServer(serverApp)
	port = basePort + pid
	server.listen(port)
	print("Binding backend server on port: " + str(port) + " in processID " + str(pid))

#Generate the port numbers in a round-robin
#fashion to load balance between the
#different servers
def RoundRobinPortGenerator(portRange):
	length = len(portRange)

	index = 0
	while True:
		yield portRange[index]
		index = (index + 1) % length

#Load balancer class
#Whenever a request is received, it is forwarded to
#one of the backend servers in an asynchronous form
class FrontendHandler(web.RequestHandler):
	_portGenerator = RoundRobinPortGenerator([basePort+1, basePort+2, basePort+3])
	_hostname = None

	def initialize(self):
		if FrontendHandler._hostname is None:
			index = self.request.host.index(':')
			FrontendHandler._hostname = self.request.host[:index]

	@gen.coroutine
	def get(self):
		#Simple Hello World application
		http_client = httpc.AsyncHTTPClient()
		try:
			response = yield http_client.fetch( \
				"http://" + FrontendHandler._hostname + ":" +  \
				str(next(FrontendHandler._portGenerator)) + "/")
			self.write(response.body)
		except httpc.HTTPError as e:
			self.write("HTTP Error: " + str(e))
		except Exception as e:
			self.write("Server Error: " + str(e))
		http_client.close()

#Start the Load Balancer
if pid == 0:
	loadBalancerApp = web.Application([
		(r"/", FrontendHandler)
	])

	frontend = https.HTTPServer(loadBalancerApp)
	port = basePort

	print("Binding Frontend server on port: " + str(port) + " in processID: " + str(pid))
	frontend.listen(port)

#Start the ioloop to listen to start 
#event listening
iol.IOLoop.current().start()
