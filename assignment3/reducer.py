from tornado.ioloop import IOLoop
from tornado import gen, httpclient, web
import json, urllib, subprocess

class Reducer(web.RequestHandler):
    
    @gen.coroutine
    def get(self):
        reducer_ix = int(self.get_query_argument("reduce_ix", default="0"))
        reducer_path = self.get_query_argument("reducer_path", default="wordcount/reducer.py")
        map_task_ids = (self.get_query_argument("reducer_path", 
            default="8a97fd755ea12827485749036e15d651,d3486112191e4717d17d4fba189bdbf6")).split(',')
        job_path = self.get_query_argument("job_path", default="fish_jobs")
        servers = ["linserv2.cims.nyu.edu:34514", "linserv2.cims.nyu.edu:34515"]
        num_mappers = len(map_task_ids)

        http = httpclient.AsyncHTTPClient()
        futures = []
        for i in range(num_mappers):
            server = servers[i % len(servers)]
            params = urllib.parse.urlencode({'reducer_ix': reducer_ix,
                                             'map_task_id': map_task_ids[i]})
            url = "http://%s/retrieve_map_output?%s" % (server, params)
            futures.append(http.fetch(url))
        responses = yield futures

        kv_pairs = []
        for r in responses:
            print(json.loads(r.body.decode()))
            kv_pairs.extend(json.loads(r.body.decode()))
        kv_pairs.sort(key=lambda x: x[0])

        kv_string = "\n".join([pair[0] + "\t" + pair[1] for pair in kv_pairs])
        p = subprocess.Popen(reducer_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        (out, _) = p.communicate(kv_string.encode())
        print(out.decode())

        self.write(json.encode({'status': 'success'}))

if __name__ == "__main__":
    app = web.Application([
            (r"/reduce", Reducer)
        ])

    app.listen(12345)
    print("Started reducer on 12345")

    IOLoop.current().start()
