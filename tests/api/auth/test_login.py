import uuid

import pytest
import allure
from faker import Faker
from backend.api.services.auth.client.models.login_request import LoginRequest
from utils.exceptions import ApiError
from utils.constants import HTTPStatus

faker = Faker()


@allure.epic("Auth API")
@allure.feature("Логин")
class TestLoginPositive:
    """Позитивные сценарии"""

    @allure.story("Позитивные сценарии")
    @allure.title("Успешный логин")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_login_success(self, auth_service_anonym, registered_user, soft_assert):
        login = registered_user["login"]
        password = registered_user["password"]

        response = auth_service_anonym.login_user(
            LoginRequest(
                login=login,
                password=password
            )
        )

        soft_assert.assert_true(response.access_token is not None, "access_token не должен быть None")
        soft_assert.assert_equal(response.user.email, registered_user["email"], "email не совпадает")
        soft_assert.assert_equal(response.user.id, registered_user["user_id"], "user_id не совпадает")


@allure.epic("Auth API")
@allure.feature("Логин")
class TestLoginNegative:
    """Негативные сценарии логина"""

    WRONG_PASSWORD = faker.password(
        length=5,
        digits=False
    )
    EXPECTED_STATUS_WRONG_PASSWORD = HTTPStatus.UNAUTHORIZED

    NONEXISTENT_USER_LOGIN = uuid.uuid4().hex
    EXPECTED_STATUS_NONEXISTENT_USER = HTTPStatus.UNAUTHORIZED

    ANY_PASSWORD = faker.password()
    EXPECTED_STATUS_EMPTY_PASSWORD = HTTPStatus.UNAUTHORIZED
    EXPECTED_STATUS_EMPTY_LOGIN = HTTPStatus.UNAUTHORIZED

    @allure.story("Негативные сценарии")
    @allure.title("Логин с неверным паролем")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_wrong_password(self, auth_service_anonym, registered_user):
        login = registered_user["login"]

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.login_user(
                LoginRequest(
                    login=login,
                    password=self.WRONG_PASSWORD
                )
            )

        actual_status = exc_info.value.status_code

        assert actual_status == self.EXPECTED_STATUS_WRONG_PASSWORD, \
            f"Expected: {self.EXPECTED_STATUS_WRONG_PASSWORD}\n" \
            f"Actual: {actual_status}"

    @allure.story("Негативные сценарии")
    @allure.title("Логин с несуществующим пользователем")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_nonexistent_user(self, auth_service_anonym):
        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.login_user(
                LoginRequest(
                    login=self.NONEXISTENT_USER_LOGIN,
                    password=self.ANY_PASSWORD
                )
            )
        actual_status = exc_info.value.status_code

        assert actual_status == self.EXPECTED_STATUS_NONEXISTENT_USER, \
            f"Expected: {self.EXPECTED_STATUS_NONEXISTENT_USER}\n" \
            f"Actual: {actual_status}"

    @allure.story("Негативные сценарии")
    @allure.title("Логин с пустым login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_empty_login(self, auth_service_anonym):
        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.login_user_raw(
                data={
                    "login": "",
                    "password": self.ANY_PASSWORD
                }
            )
        actual_status = exc_info.value.status_code
        assert actual_status == self.EXPECTED_STATUS_EMPTY_LOGIN, \
            f"Expected: {self.EXPECTED_STATUS_EMPTY_LOGIN}\n" \
            f"Actual: {actual_status}"

    @allure.story("Негативные сценарии")
    @allure.title("Логин с пустым паролем")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_empty_password(self, auth_service_anonym, registered_user):
        login = registered_user["login"]

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.login_user_raw(
                data={
                    "login": login,
                    "password": ""
                }
            )
        actual_status = exc_info.value.status_code
        assert actual_status == self.EXPECTED_STATUS_EMPTY_PASSWORD
