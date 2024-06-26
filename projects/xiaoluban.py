import pprint
import urllib.parse

import requests

from requests.status_codes import codes as status


class ISCLDistributor:
    def __init__(self, base_url: str, api1: str = None, api2: str = None):
        self.base_url = base_url.endswith("/") and base_url or base_url + "/"
        self.api1 = self._process_api_format(api1)
        self.api2 = self._process_api_format(api2)

    @classmethod
    def _process_api_format(cls, api):
        if not api:
            return api
        return api.startswith("/") and api.replace("/", "", 1) or api

    @classmethod
    def _check_status_ok(cls, response):
        if response.status_code != status.ok:
            raise requests.exceptions.HTTPError(f"response.status_code{response.status_code} != {status.ok}")

    def get_one_record(self, query=None, api=None):
        api = self._process_api_format(api) or self.api1
        url = self.base_url + api
        if query:
            url += "?" + urllib.parse.urlencode(query)
        response = requests.get(url, verify=False)
        self._check_status_ok(response)
        return response.json()

    def distribute(self, data, api=None):
        api = self._process_api_format(api) or self.api2
        url = self.base_url + api
        response = requests.post(url, json=data, verify=False)
        self._check_status_ok(response)
        return response.json()


class PreValidation(ISCLDistributor):
    pass


pre_validation = PreValidation("https://httpbin.org/", "get", "post")
pprint.pprint(pre_validation.get_one_record(query={
    "name": "zsh"
}))
pprint.pprint(pre_validation.distribute(data={
    "employee_id": "213191443"
}))
