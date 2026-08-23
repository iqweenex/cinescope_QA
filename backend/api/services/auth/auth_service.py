from backend.api.services.auth.client.models.login_request_raw import LoginRequestRaw
from backend.api.services.auth.client.models.register_request_raw import RegisterRequestRaw
from backend.api.services.general.base_service import BaseService
from backend.api.services.auth.client.helpers.authorization_helper import AuthorizationHelper
from backend.api.services.auth.user_admin.helpers.user_helper import UserHelper
from backend.api.services.auth.client.models.login_request import LoginRequest
from backend.api.services.auth.client.models.login_response import LoginResponse
from backend.api.services.auth.client.models.register_request import RegisterRequest
from backend.api.services.auth.client.models.register_response import RegisterResponse
from backend.api.services.auth.user_admin.models.create_user_request import CreateUserRequest
from backend.api.services.auth.user_admin.models.edit_user_request import EditUserRequest
from backend.api.services.auth.user_admin.models.admin_user_response import UserResponse
from backend.api.services.auth.user_admin.models.find_all_users_response import FindAllUsersResponse

from utils.api_utils import ApiUtils
from config import Config


class AuthService(BaseService):
    SERVICE_URL = Config.AUTH_SERVICE_URL

    def __init__(self, api_utils: ApiUtils):
        super().__init__(api_utils)
        self.authorization_helper = AuthorizationHelper(self.api_utils)
        self.user_helper = UserHelper(self.api_utils)

    def register_user(self, register_request: RegisterRequest) -> RegisterResponse:
        response = self.authorization_helper.post_register(data=register_request.model_dump(by_alias=True))
        return RegisterResponse(**response.json())

    def register_user_raw(self, register_request: RegisterRequestRaw) -> dict:
        """
        Отправляет запрос на регистрацию без валидации данных.
        Используется только в негативных тестах.
        """
        response = self.authorization_helper.post_register(
            data=register_request.model_dump(by_alias=True)
        )
        return response.json()

    def login_user_raw(self, login_request: LoginRequestRaw) -> dict:
        """
        Отправляет запрос на регистрацию без валидации данных.
        Используется только в негативных тестах.
        """
        response = self.authorization_helper.post_register(
            data=login_request.model_dump(by_alias=True)
        )
        return response.json()

    def login_user(self, login_request: LoginRequest) -> LoginResponse:
        response = self.authorization_helper.post_login(data=login_request.model_dump(by_alias=True))
        return LoginResponse(**response.json())

    def logout_user(self):
        response = self.authorization_helper.get_logout()
        return response

    def refresh_tokens(self) -> dict:
        response = self.authorization_helper.get_refresh()
        return response.json()

    def confirm_email(self, token: str) -> dict:
        response = self.authorization_helper.get_confirm(token=token)
        return response.json()

    def create_user_by_admin(self, create_request: CreateUserRequest) -> UserResponse:
        response = self.user_helper.post_create_user(data=create_request.model_dump(by_alias=True))
        return UserResponse(**response.json())

    def get_user_by_admin(self, id_or_email: str) -> UserResponse:
        response = self.user_helper.get_user_by_id_or_email(id_or_email)
        return UserResponse(**response.json())

    def edit_user_by_admin(self, user_id: str, edit_request: EditUserRequest) -> UserResponse:
        response = self.user_helper.patch_user(user_id, data=edit_request.model_dump(by_alias=True))
        return UserResponse(**response.json())

    def delete_user_by_admin(self, user_id: str) -> UserResponse:
        response = self.user_helper.delete_user(user_id)
        return UserResponse(**response.json())

    def get_all_users_by_admin(self, **kwargs) -> FindAllUsersResponse:
        formatted_filters = {}
        for key, value in kwargs.items():
            parts = key.split('_')
            camel_key = parts[0] + ''.join(p.capitalize() for p in parts[1:])
            formatted_filters[camel_key] = value

        response = self.user_helper.get_all_users(filters=formatted_filters)
        return FindAllUsersResponse(**response.json())
