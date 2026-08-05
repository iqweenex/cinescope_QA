import pytest
from faker import Faker
from logger.logger import Logger
from utils.api_utils import ApiUtils
from backend.api.services.auth.auth_service import AuthService
from backend.api.services.auth.client.models.login_request import LoginRequest
from backend.api.services.auth.client.models.register_request import RegisterRequest
from config import Config

faker = Faker()


@pytest.fixture(scope='session')
def auth_api_utils_anonym() -> ApiUtils:
    return ApiUtils(url=AuthService.SERVICE_URL)


@pytest.fixture(scope='session')
def auth_service_anonym(auth_api_utils_anonym) -> AuthService:
    return AuthService(api_utils=auth_api_utils_anonym)


@pytest.fixture(scope='session')
def admin_api_utils(auth_service_anonym) -> ApiUtils:
    Logger.info(f"Логин администратора: {Config.ADMIN_EMAIL}")

    login_response = auth_service_anonym.login_user(
        LoginRequest(
            email=Config.ADMIN_EMAIL,
            password=Config.ADMIN_PASSWORD
        )
    )

    return ApiUtils(
        url=AuthService.SERVICE_URL,
        headers={"Authorization": f"Bearer {login_response.access_token}"}
    )


@pytest.fixture(scope='session')
def auth_service_admin(admin_api_utils) -> AuthService:
    return AuthService(api_utils=admin_api_utils)


@pytest.fixture(scope='session')
def test_user_credentials():
    return {
        "email": faker.email(),
        "password": faker.password(
            length=12,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True
        ),
        "full_name": faker.name()
    }


@pytest.fixture(scope='session')
def registered_user(auth_service_anonym, test_user_credentials) -> dict:
    email = test_user_credentials["email"]
    password = test_user_credentials["password"]
    full_name = test_user_credentials["full_name"]

    Logger.info(f"Регистрация тестового пользователя: {email}")

    # Регистрация
    auth_service_anonym.register_user(
        RegisterRequest(
            email=email,
            full_name=full_name,
            password=password,
            password_repeat=password
        )
    )

    # Логин для получения токенов
    login_response = auth_service_anonym.login_user(
        LoginRequest(email=email, password=password)
    )

    Logger.info(f"Тестовый пользователь зарегистрирован и авторизован: {email}")

    return {
        "email": email,
        "password": password,
        "full_name": full_name,
        "access_token": login_response.access_token,
        "refresh_token": login_response.refresh_token,
        "user_id": login_response.user.id
    }


@pytest.fixture(scope='session')
def user_api_utils(registered_user) -> ApiUtils:
    return ApiUtils(
        url=AuthService.SERVICE_URL,
        headers={"Authorization": f"Bearer {registered_user['access_token']}"}
    )


@pytest.fixture(scope='session')
def auth_service_user(user_api_utils) -> AuthService:
    return AuthService(api_utils=user_api_utils)
