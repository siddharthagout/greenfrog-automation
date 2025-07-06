import requests


class BaseApiClient:
    def __init__(self, base_url, headers=None, auth=None):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {"Content-Type": "application/json"}
        self.auth = auth  # (username, password) tuple if needed

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return requests.get(url, headers=self.headers, params=params, auth=self.auth)

    def post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return requests.post(url, headers=self.headers, json=data, auth=self.auth)

    def put(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return requests.put(url, headers=self.headers, json=data, auth=self.auth)

    def delete(self, endpoint):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return requests.delete(url, headers=self.headers, auth=self.auth)
