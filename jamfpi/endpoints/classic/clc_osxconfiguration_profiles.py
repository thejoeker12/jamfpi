"""Endpoints for configuration profiles"""
from ..endpoint_parent import Endpoint
from requests import Request

class ConfigurationProfiles(Endpoint):
    """Configuration profiles object"""
    _suffix = "/osxconfigurationprofiles"

    def get_all(self, accept_format: str = "xml"):
        if accept_format.lower() not in ["json", "xml"]:
            raise ValueError("Invalid accept format provided (allowed: 'xml', 'json'): %s", accept_format)
        
        url = self._api.url() + self._suffix
        headers = self._api.header(f"basic-{accept_format}")
        req = Request("GET", url=url, headers=headers)
        resp = self._api.do(req)
        return resp

    def get_by_id(self, id: int, accept_format: str = "xml"):
        if accept_format.lower() not in ["json", "xml"]:
            raise ValueError("Invalid accept format provided (allowed: 'xml', 'json'): %s", accept_format)

        url = self._api.url() + self._suffix + f"/id/{id}"
        headers = self._api.header(f"basic-{accept_format}")
        req = Request("GET", url=url, headers=headers)
        resp = self._api.do(req)
        return resp
    

    def update_by_id(self, id: int, updatedConfiguration: str):
        url = self._api.url() + self._suffix + f"/id/{id}"
        headers = self._api.header("put")
        req = Request("PUT", url=url, headers=headers, data=updatedConfiguration)
        resp = self._api.do(req)
        return resp
    

    def create(self, config_profile: str):
        url = self._api.url() + self._suffix + "/id/0"
        headers = self._api.header("post")
        req = Request("POST", url=url, headers=headers, data=config_profile)
        resp = self._api.do(req)
        return resp
    

    def delete_by_id(self, id: int):
        url = self._api.url() + self._suffix + ("/id/%s" % id)
        headers = self._api.header("basic-json")
        req = Request("DELETE", url, headers=headers)
        resp = self._api.do(req)
        return resp





