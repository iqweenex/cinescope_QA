import pytest
from uuid import uuid4
from faker import Faker
from logger.logger import Logger
from utils.api_utils import ApiUtils
from backend.api.services.auth.auth_service import AuthService
from backend.api.services.auth.client.models.login_request import LoginRequest
from backend.api.services.auth.client.models.register_request import RegisterRequest
from config import Config
from utils.soft_assert import SoftAssert

faker = Faker()


@pytest.fixture(scope='session')
def auth_api_utils_anonym() -> ApiUtils:
    return ApiUtils(url=AuthService.SERVICE_URL)


@pytest.fixture(scope='session')
def auth_service_anonym(auth_api_utils_anonym) -> AuthService:
    return AuthService(api_utils=auth_api_utils_anonym)


@pytest.fixture(scope='session')
def test_user_credentials():
    return {
        "login": faker.user_name(),
        "email": faker.email(),
        "password": faker.password(
            length=12,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True
        )
    }


@pytest.fixture
def user_data_factory():
    def _factory(**overrides):
        unique_id = uuid4().hex
        return {
            "login": unique_id,
            "email": f"{unique_id}@example.com",
            "password": faker.password(
                length=12,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True
            ),
            **overrides
        }

    return _factory


@pytest.fixture(scope='session')
def registered_user(auth_service_anonym, test_user_credentials) -> dict:
    login = test_user_credentials["login"]
    email = test_user_credentials["email"]
    password = test_user_credentials["password"]

    Logger.info(f"Регистрация тестового пользователя: login={login}, email={email}")

    response = auth_service_anonym.register_user(
        RegisterRequest(
            login=login,
            email=email,
            password=password
        )
    )

    Logger.info(f"Тестовый пользователь зарегистрирован {email}")

    return {
        "login": login,
        "email": email,
        "password": password,
        "user_id": response.id
    }


@pytest.fixture(scope='session')
def logged_in_user(auth_service_anonym, registered_user) -> dict:
    login = registered_user["login"]
    password = registered_user["password"]

    Logger.info(f"Авторизация тестового пользователя: login={login}")

    login_response = auth_service_anonym.login_user(
        LoginRequest(
            login=login,
            password=password
        )
    )

    refresh_token = auth_service_anonym.api_utils.session.cookies.get("refresh_token")

    return {
        **registered_user,
        "access_token": login_response.access_token,
        "refresh_token": refresh_token
    }


@pytest.fixture(scope='function')
def auth_service_factory():
    def _factory(refresh_token=None):
        cookies = {"refresh_token": refresh_token} if refresh_token else None
        return AuthService(ApiUtils(
            url=AuthService.SERVICE_URL,
            cookies=cookies
        ))

    return _factory


@pytest.fixture(scope='session')
def user_api_utils(logged_in_user) -> ApiUtils:
    return ApiUtils(
        url=AuthService.SERVICE_URL,
        headers={"Authorization": f"Bearer {logged_in_user['access_token']}"}
    )


@pytest.fixture(scope='session')
def auth_service_user(user_api_utils) -> AuthService:
    return AuthService(api_utils=user_api_utils)


@pytest.fixture(scope="function")
def soft_assert():
    soft = SoftAssert()
    yield soft
    soft.assert_all()
