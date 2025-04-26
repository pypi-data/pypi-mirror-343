"""
    DNS Authenticator for Hurricane Electric.
"""

import requests
import zope.interface
from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    description = ('Obtain certificates using preconfigured TXT records at Hurricane Electric DNS.')

    @classmethod
    def add_parser_arguments(cls, add):
        super().add_parser_arguments(add)
        add('key', help='DDNS Key for _acme-challenge.<domain>', required=True)

    def _setup_credentials(self):
        pass

    def _perform(self, domain, validation_name, validation):
        try:
            r = requests.post("https://dyn.dns.he.net/nic/update", data={
                "hostname": validation_name,
                "password": self.conf('key'),
                "txt": validation
            })
            if r.text not in ('good', 'nochg'): # always returns 200/OK
                raise errors.PluginError(f"Error returned from HE: {r.text}")
        except requests.RequestException as e:
            raise errors.PluginError(e)

    def _cleanup(self, domain, validation_name, validation):
        self._perform(domain, validation_name, "-")
