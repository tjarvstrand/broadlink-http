from BaseHTTPServer import HTTPServer

class Server(HTTPServer):

    def __init__(self, address, handler, config):
        self.config = config
        HTTPServer.__init__(self, address, handler)
