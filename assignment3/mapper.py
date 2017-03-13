from tornado import web, gen

class Map(web.RequestHandler):

    @gen.coroutine
    def get(self):
        self.write("I am in Map")

class Output(web.RequestHandler):

    @gen.coroutine
    def get(self):
        self.write("I am in Map output")

if __name__ == "__main__":
    pass