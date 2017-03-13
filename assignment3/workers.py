# -*- coding: UTF-8 -*-
'''
Name: Chirag Maheshwari
Course: Search Engine Architecture

Workers
Main Job is to start the workers as 
reducers and mappers and print out their
hostnames on the console.
The servers run on different forked subprocesses
'''
import mapper, reducer
import inventory

from tornado.ioloop import IOLoop as iol
from tornado import web, process as proc

class WorkerServer(object):
	def __init__(self, port):
		self.__app = None
		self.__port = port

	def start(self):
		if self.__app is None:
			try:
				app = web.Application([
					(r'/reduce', reducer.Reduce),
					(r'/retrieve_reduce_output', reducer.Output),
					(r'/map', mapper.Map),
					(r'/retrieve_map_output', mapper.Output)])
				app.listen(self.__port)
			except Exception as e:
				print(e)
				print("Cannot start server on port: ", self.__port)
				return False

			self.__app = app
		return True


def start_workers():
	pid = proc.fork_processes(inventory.NUM_WORKERS)

	if WorkerServer(inventory.WORKER_PORTS[pid]).start():
		print("Started Worker on port: ", inventory.WORKER_PORTS[pid], "with sub-process-id: ", pid)
	iol.current().start()

if __name__ == "__main__":
	start_workers()