from requests import Request
from ..endpoint_parent import Endpoint

class SsoCertificates(Endpoint):
    # // TODO docstring
    _uri = "/sso/cert"

    def get_certificate(self):
        # // TODO docstring
        url = self._api.url("1") + self._uri
        headers = self._api.header("basic-json")
        request = Request("GET", url=url, headers=headers)
        call = self._api.do(request)
        return call
