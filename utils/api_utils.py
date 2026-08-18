import json
import curlify
import requests
from requests import Session
from logger.logger import Logger
from utils.json_utils import JsonUtils
from utils.exceptions import ApiError


def log_response(func):
    def _log_response(*args, **kwargs) -> requests.Response:
        response = func(*args, **kwargs)
        Logger.info(f"Request: {curlify.to_curl(response.request)}")
        body = json.dumps(response.json(), indent=2, ensure_ascii=False) if JsonUtils.is_json(
            response.text) else response.text
        Logger.info(f"Response status code='{response.status_code}', elapsed_time='{response.elapsed}'\n{body}\n")

        # Если статус-код >= 400 — выбрасываем ApiError
        if response.status_code >= 400:
            error_data = response.json() if JsonUtils.is_json(response.text) else {"message": response.text}
            error_messages = error_data.get("message", [error_data.get("error", response.text)])
            if isinstance(error_messages, str):
                error_messages = [error_messages]
            raise ApiError(response.status_code, error_messages)

        return response

    return _log_response


class ApiUtils:
    def __init__(self, url, headers=None):
        if headers is None:
            headers = {}
        self.session = Session()
        self.session.headers.update(headers)
        self.url = url

    @log_response
    def get(self, endpoint_url, **kwargs):
        response = self.session.get(self.url + endpoint_url, **kwargs)
        return response

    @log_response
    def post(self, endpoint_url, data=None, json=None, **kwargs):
        response = self.session.post(self.url + endpoint_url, data=data, json=json, **kwargs)
        return response

    @log_response
    def put(self, endpoint_url, data=None, json=None, **kwargs):
        response = self.session.put(self.url + endpoint_url, data=data, json=json, **kwargs)
        return response

    @log_response
    def delete(self, endpoint_url, **kwargs):
        response = self.session.delete(self.url + endpoint_url, **kwargs)
        return response

    @log_response
    def patch(self, endpoint_url, data=None, json=None, **kwargs):
        response = self.session.patch(self.url + endpoint_url, data=data, json=json, **kwargs)
        return response
