# -*- coding: UTF-8 -*-
'''
Name: Chirag Maheshwari
Course: Search Engine Architecture

Reducer
Handlers the reduce request
'''
from tornado import web, gen, httpclient as httpc
import json, os, urllib, subprocess
import inventory

class Reduce(web.RequestHandler):
	def _fetch_arguments(self):
		self._map_task_ids = (self.get_query_argument(
			"map_task_ids", 
			default="0", 
			strip=False)).split(',')

		self._reducer_id = int(self.get_query_argument(
			"reducer_ix",
			default="0",
			strip=False))

		self._reducer_path = self.get_query_argument(
			"reducer_path",
			default="wordcount/reducer.py",
			strip=False)

		self._job_path = self.get_query_argument(
			"job_path",
			default="fish_jobs",
			strip=False)

	def _emit_data(self, responses):
		kv_pairs = []
		for r in responses:
			print(r)
			kv_pairs.extend(json.loads(r.body.decode()))
		kv_pairs.sort(key=lambda x:x[0])

		kv_string = "\n".join([p[0] + '\t' + p[1] for p in kv_pairs])
		(out, _) = subprocess.Popen(
			self._reducer_path, 
			stdin=subprocess.PIPE, 
			stdout=subprocess.PIPE).communicate(
				kv_string.encode())
		out = out.decode()

		with open(os.path.join(self._job_path, str(self._reducer_id) + ".out"), "w") as f:
			f.write(out)
			self._status = True

	@gen.coroutine
	def _get_maps(self):
		self._status = False

		client = httpc.AsyncHTTPClient()
		futures = []
		for i in range(len(self._map_task_ids)):
			server = inventory.WORKER_HOSTS[i % inventory.NUM_WORKERS]
			params = urllib.parse.urlencode({
				'reducer_ix': self._reducer_id,
				'map_task_id': self._map_task_ids[i]})
			url = "http://{}/retrieve_map_output?{}".format(
				server, params)
			futures.append(client.fetch(url))
		responses = yield futures

		return responses

	def _get_response(self):
		if self._status:
			return {'status': 'success'}
		else:
			return {'status': 'failure'}

	@gen.coroutine
	def get(self):
		self._fetch_arguments()
		responses = yield self._get_maps()
		self._emit_data(responses)
		response = self._get_response()
		print(response)
		self.write(response)

class Output(web.RequestHandler):
	def _fetch_arguments(self):
		self._job_path = self.get_query_argument(
			"job_path",
			default="fish_jobs",
			strip=False)

		self._num_reducers = int(self.get_query_argument(
			"num_reducers",
			default="1",
			strip=False))

	def _get_response(self):
		lines = []
		for filename in os.listdir(self._job_path):
			if filename.endswith(".out"):
				f = os.path.join(self._job_path, filename)
				lines.append(f + ":")
				for line in open(f, "r"):
					lines.append(line)
				lines.append(" ")

		return "<br />".join(lines)

	@gen.coroutine
	def get(self):
		self._fetch_arguments()
		response = self._get_response()
		print(response)
		self.write(response)

if __name__ == "__main__":
    pass