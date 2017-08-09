#!/usr/bin/env python2

# File: https_wrapper.py
# a minimal HTTPS wrapper for HTTP requests

import SocketServer
import SimpleHTTPServer
import urllib2
import sys

class Wrapper(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("get:", self.path)
        url = host + self.path
        req = urllib2.Request(url)
        for header, value in self.headers.items():
            if header == "host":
                continue
            req.add_header(header, value)

        self.copyfile(urllib2.urlopen(req), self.wfile)


if len(sys.argv) < 3:
    print >> sys.stderr, "usage: " + sys.argv[0] + " PORT HOST"
    sys.exit(1)
port = int(sys.argv[1])
host = sys.argv[2]

print("listening port....", port)
SocketServer.ForkingTCPServer.allow_reuse_address = 1
server = SocketServer.ForkingTCPServer(('', port), Wrapper)
server.allow_reuse_address = True
server.serve_forever()
