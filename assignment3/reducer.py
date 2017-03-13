from tornado import web, gen

class Reduce(web.RequestHandler):

    @gen.coroutine
    def get(self):
        self.write("I am in reduce")

class Output(web.RequestHandler):

    @gen.coroutine
    def get(self):
        self.write("I am in reduce output")

if __name__ == "__main__":
    pass