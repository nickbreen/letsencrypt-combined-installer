"""Haproxy Let's Encrypt authenticator plugin."""

import os
import logging
import re
import subprocess

import zope.component
import zope.interface

import threading
import time

from acme import challenges

from letsencrypt import errors
from letsencrypt import interfaces
from letsencrypt.plugins import common

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer


# This is the port where HAproxy should forward requests to
PORT_NUMBER = 8080


logger = logging.getLogger(__name__)

class HaProxyHandler(BaseHTTPRequestHandler):
    validation = ''

    def do_GET(self):
       self.send_response(200)
       self.send_header('Content-Type','text/html')
       self.end_headers()
       # Send the html message
       self.wfile.write(self.validation.encode())
       return



class Authenticator(common.Plugin):

    zope.interface.implements(interfaces.IAuthenticator)
    zope.interface.classProvides(interfaces.IPluginFactory)

    description = "Haproxy Authenticator"
    instance = ""

#    @classmethod
#    def add_parser_arguments(cls, add):
#        add("port", default=os.getenv('PORT'),
#            help="Haproxy redirect port")

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self._httpd = None

    def prepare(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return ("")

    def get_chall_pref(self, domain):
        # pylint: disable=missing-docstring,no-self-use,unused-argument
        return [challenges.HTTP01]

    def perform(self, achalls):  # pylint: disable=missing-docstring
        responses = []
        for achall in achalls:
            responses.append(self._perform_single(achall))
        return responses

    def _perform_single(self, achall):

        
	# Get a request handler
        handler = HaProxyHandler;

        # Put validation key in handler
        handler.validation = validation

        # Create webserver with this handler
        server = HTTPServer(('', PORT_NUMBER), HaProxyHandler)

        # Start webserver in seperate thread
        thread = threading.Thread(target=server.serve_forever)
        thread.start()

        # Save the server in this object
        self.instance = server

        # Allow server to boot
        time.sleep( 2 )

        if response.simple_verify(
                achall.chall, achall.domain,
                achall.account_key.public_key(), self.config.http01_port):
            return response
        else:
            logger.error(
                "Self-verify of challenge failed, authorization abandoned!")
            return None


    def cleanup(self, achalls):

        # Shutdown the webserver
        self.instance.shutdown()
        return None
