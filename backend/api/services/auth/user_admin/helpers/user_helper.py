import requests
from backend.api.services.general.helpers.base_helper import BaseHelper


class UserHelper(BaseHelper):
    ENDPOINT_PREFIX = "/user"
    _USER_BY_ID_TEMPLATE = "/user/{}"

    def get_all_users(self, filters: dict = None) -> requests.Response:
        params = filters if filters is not None else {}
        return self.api_utils.get(self.ENDPOINT_PREFIX, params=params)

    def get_user_by_id_or_email(self, id_or_email: str) -> requests.Response:
        return self.api_utils.get(f"{self.ENDPOINT_PREFIX}/{id_or_email}")

    def post_create_user(self, data: dict) -> requests.Response:
        return self.api_utils.post(self.ENDPOINT_PREFIX, json=data)

    def patch_user(self, user_id: str, data: dict) -> requests.Response:
        return self.api_utils.patch(self._USER_BY_ID_TEMPLATE.format(user_id), json=data)

    def delete_user(self, user_id: str) -> requests.Response:
        return self.api_utils.delete(self._USER_BY_ID_TEMPLATE.format(user_id))
