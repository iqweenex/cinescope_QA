import requests
from backend.api.services.general.helpers.base_helper import BaseHelper


class AuthorizationHelper(BaseHelper):
    REGISTER_ENDPOINT = "/register"
    LOGIN_ENDPOINT = "/login"
    LOGOUT_ENDPOINT = "/logout"
    REFRESH_ENDPOINT = "/refresh-tokens"
    CONFIRM_ENDPOINT = "/confirm"

    def post_register(self, data: dict) -> requests.Response:
        return self.api_utils.post(self.REGISTER_ENDPOINT, json=data)

    def post_login(self, data: dict) -> requests.Response:
        return self.api_utils.post(self.LOGIN_ENDPOINT, json=data)

    def get_logout(self) -> requests.Response:
        return self.api_utils.get(self.LOGOUT_ENDPOINT)

    def get_refresh(self) -> requests.Response:
        return self.api_utils.get(self.REFRESH_ENDPOINT)

    def get_confirm(self, token: str) -> requests.Response:
        return self.api_utils.get(f"{self.CONFIRM_ENDPOINT}?token={token}")
