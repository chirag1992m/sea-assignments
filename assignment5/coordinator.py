# -*- coding: utf-8 -*-

import argparse, os, importlib, inventory, urllib, io
import cloudpickle, pickle
from tornado import httpclient as httpc, gen
from tornado.ioloop import IOLoop

def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", type=str, required=True, default='apps.word2vec')
    parser.add_argument("--job_path", type=str, required=True, default='w2v_jobs')
    parser.add_argument("--iterations", type=int, required=True, default=50)
    
    return parser.parse_args()

def get_input_files(options):
    path = options.job_path
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.in')]

@gen.coroutine
def main():
    options = get_options()
    input_files = get_input_files(options)

    application = importlib.import_module(options.app)
    model = application.init_model(input_files)

    client = httpc.AsyncHTTPClient()

    for i in range(options.iterations):
        futures = []
        worker_index = 0
        for f in input_files:
            server = inventory.WORKER_HOSTS[worker_index % inventory.NUM_WORKERS]
            params = urllib.parse.urlencode({
                'input_file': f})
            body = cloudpickle.dumps((application.compute_gradient, model))
            url = "http://{}/compute_gradient?{}".format(
                server, params)
            futures.append(client.fetch(url, method='POST', body=body))
            worker_index += 1

        responses = yield futures

        for r in responses:
            stream = io.BytesIO(r.body)
            gradient = pickle.load(stream)
            application.update_model(model, gradient)
        print("iteration {} done!".format(i))

    pickle.dump(model, open(os.path.join(options.job_path, '0.out'), 'wb'))
    client.close()

if __name__ == "__main__":
    IOLoop.current().run_sync(main)