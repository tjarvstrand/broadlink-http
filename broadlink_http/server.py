from BaseHTTPServer import HTTPServer

class Server(HTTPServer):

    def __init__(self, address, handler, config, logger):
        self.config = config
        self.logger = logger
        HTTPServer.__init__(self, address, handler)
