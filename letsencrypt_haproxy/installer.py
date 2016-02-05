"""HAproxy  Let's Encrypt installer plugin."""
import os
import sys
import logging
import re
import subprocess

import zope.component
import zope.interface

from subprocess import call
from acme import challenges

from letsencrypt import errors
from letsencrypt import interfaces
from letsencrypt.plugins import common


logger = logging.getLogger(__name__)

class Installer(common.Plugin):
    zope.interface.implements(interfaces.IInstaller)
    zope.interface.classProvides(interfaces.IPluginFactory)

    description = "Haproxyt Installer"

    @classmethod
    def add_parser_arguments(cls, add):
        add("cf-distribution-id", default=os.getenv('CF_DISTRIBUTION_ID'),
            help="CloudFront distribution id")

    def __init__(self, *args, **kwargs):
        super(Installer, self).__init__(*args, **kwargs)


    def prepare(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return ("")

    def get_all_names(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def deploy_cert(self, domain, cert_path, key_path, chain_path, fullchain_path):

        path = os.path.dirname(cert_path)


        # Write key, cert & chain in one file 
        combined = open(path + "/combined.pem", "w")
        key = open(key_path, "r")
        combined.write(key.read())
        key.close()

        cert = open(cert_path, "r")
        combined.write(cert.read())
        cert.close()

        chain = open(chain_path, "r")
        combined.write(chain.read())
        chain.close()

        combined.close()


        # Read haproxy
        hawrite = open("/tmp/haproxy.cfg", "w")
        compare = "## LE-BIND " + domain
        with open('/etc/haproxy/haproxy.cfg') as haread:
            for line in haread:
                if (re.match(".*## LE-BIND " + domain, line)):
                    hawrite.write("bind *:443 ssl crt " + path + "/combined.pem" + " ## LE-BIND " + domain + "\n")
                else:
                    hawrite.write(line)    

        hawrite.close()

	os.rename("/etc/haproxy/haproxy.cfg", "/etc/haproxy/haproxy.cfg.bak")
	os.rename("/tmp/haproxy.cfg", "/etc/haproxy/haproxy.cfg")

        pass


    def enhance(self, domain, enhancement, options=None):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def supported_enhancements(self):  # pylint: disable=missing-docstring,no-self-use
        return []  # pragma: no cover

    def get_all_certs_keys(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def save(self, title=None, temporary=False):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def rollback_checkpoints(self, rollback=1):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def recovery_routine(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def view_config_changes(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def config_test(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def restart(self):  # pylint: disable=missing-docstring,no-self-use
        call(["/etc/init.d/haproxy", "restart"])
        pass  # pragma: no cover
