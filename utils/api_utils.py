import json
from curlify3 import to_curl, SENSITIVE_HEADERS
import requests
from requests import Session
from logger.logger import Logger
from utils.json_utils import JsonUtils
from utils.exceptions import ApiError

SENSITIVE_BODY_KEYS = {
    "accessToken", "access_token",
    "refreshToken", "refresh_token",
    "token", "password", "expiresIn",
}


def _mask_sensitive_data(data):
    if isinstance(data, dict):
        return {
            key: ("***" if key in SENSITIVE_BODY_KEYS else _mask_sensitive_data(value))
            for key, value in data.items()
        }
    if isinstance(data, list):
        return [_mask_sensitive_data(item) for item in data]
    return data


def log_response(func):
    def _log_response(*args, **kwargs) -> requests.Response:
        response = func(*args, **kwargs)
        Logger.info(f"Request: {to_curl(response.request, mask_headers=SENSITIVE_HEADERS)}")

        if JsonUtils.is_json(response.text):
            raw_json = response.json()
            masked_json = _mask_sensitive_data(raw_json)
            body = json.dumps(masked_json, indent=2, ensure_ascii=False)
        else:
            body = response.text


        Logger.info(f"Response status code='{response.status_code}', elapsed_time='{response.elapsed}'\n{body}\n")

        if response.status_code >= 400:
            error_data = response.json() if JsonUtils.is_json(response.text) else {"message": response.text}
            error_messages = error_data.get("message", [error_data.get("error", response.text)])
            if isinstance(error_messages, str):
                error_messages = [error_messages]
            raise ApiError(response.status_code, error_messages)

        return response

    return _log_response


class ApiUtils:
    def __init__(self, url, headers=None, cookies=None):
        if headers is None:
            headers = {}
        self.session = Session()
        self.session.headers.update(headers)
        if cookies:
            self.session.cookies.update(cookies)
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
