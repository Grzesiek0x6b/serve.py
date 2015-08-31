#!/usr/bin/python
"""
Copyright 2015, Grzesiek.k <grzesiek.0x6b@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from __future__ import print_function

import sys
from optparse import OptionParser
from os.path import abspath, expanduser, isfile

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

import cherrypy
from cherrypy.lib.static import serve_download


LOCAL_HOST = "127.0.0.1"
ANY_HOST = "0.0.0.0"
DEFAULT_PORT = 8080


class App(object):
    def __init__(self, host=LOCAL_HOST, port=DEFAULT_PORT,
                 resources=None, config=None):
        self.host = host
        self.port = port
        self.resources = resources or {}
        self.config = config or {}
      
    def start(self):
        cherrypy.server.socket_host = self.host
        cherrypy.server.socket_port = self.port
        cherrypy.tree.mount(self, "/", config={"/": self.config})
        cherrypy.engine.start()
    
    def block(self):
        cherrypy.engine.block()
    
    def stop(self):
        cherrypy.engine.stop()
    
    @cherrypy.expose
    def index(self):
        return "hello."
    
    @cherrypy.expose
    def serve(self, name):
        try:
            resource = self.resources[name]
            return serve_download(resource)
        except cherrypy.NotFound:
            raise
        except Exception:
            raise cherrypy.NotFound()
        
    def _cp_dispatch(self, vpath):
        cherrypy.request.params['name'] = vpath.pop(0)
        return self.serve


def getip():
    url = "http://myip.dnsomatic.com"
    return urlopen(url).read().decode()


if __name__ == "__main__":
    usage = "%prog [options] ALIAS=FILEPATH ..."
    description = "Set up simple http server to share files. " \
                  "Files will be downloadable from http://HOST:PORT/ALIAS"
    parser = OptionParser(usage=usage, description=description)
    parser.add_option("-a", "--addr", dest="host", action="store",
                      type="string",  default="local",
                      help="Host on which server will listen. "
                           "Predefined values: 'local' (for 127.0.0.1), "
                           "'public' (find public ip of machine), "
                           "'any' (listen on any address) "
                           "[default: %default].")
    parser.add_option("-p", "--port", dest="port", action="store", type="int",
                      default=DEFAULT_PORT,
                      help="Port on which server will listen "
                           "[default: %default].")
    (options, args) = parser.parse_args()

    options.host = {
        "any": ANY_HOST,
        "local": LOCAL_HOST,
        "public": getip()
    }.get(options.host.lower(), options.host)

    resources = {}
    split = lambda a: a.split("=", 1)
    for alias, filepath in map(split, args):
        filepath = abspath(expanduser(filepath))
        if isfile(filepath):
            resources[alias] = filepath
            print("Added http://{}:{}/{} -> {}"
                   .format(options.host, options.port, alias, filepath))
        else:
            print("File not found:", filepath, file=sys.stderr)
    
    cherrypy.config.update({'environment': 'staging'})
    app = App(host=options.host, port=options.port, resources=resources)
    app.start()
    app.block()

