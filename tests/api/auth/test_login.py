import pytest
import allure
from backend.api.services.auth.client.models.login_request import LoginRequest
from backend.api.services.auth.client.models.login_request_raw import LoginRequestRaw
from utils.exceptions import ApiError
from utils.constants import HTTPStatus
from utils.soft_assert import SoftAssert


@allure.epic("Auth API")
@allure.feature("Логин")
class TestLoginPositive:
    """Позитивные сценарии"""

    @allure.story("Позитивные сценарии")
    @allure.title("Успешный логин")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_login_success(self, auth_service_anonym, registered_user, soft_assert):
        email = registered_user["email"]
        password = registered_user["password"]

        response = auth_service_anonym.login_user(
            LoginRequest(
                email=email,
                password=password
            )
        )

        soft_assert.assert_true(response.access_token is not None)
        soft_assert.assert_true(response.access_token is not None)
        soft_assert.assert_equal(response.user.email, email)


@allure.epic("Auth API")
@allure.feature("Логин")
class TestLoginNegative:
    """Негативные сценарии логина"""

    WRONG_PASSWORD = "wrong_password"
    EXPECTED_STATUS_WRONG_PASSWORD = HTTPStatus.UNAUTHORIZED

    NONEXISTENT_USER_EMAIL = "nonexist@mail.com"
    PASSWORD_NONEXISTENT_USER = "any_password"
    EXPECTED_STATUS_NONEXISTENT_USER = HTTPStatus.UNAUTHORIZED

    ANY_PASSWORD = "any_password"
    EXPECTED_STATUS_EMPTY_PASSWORD = HTTPStatus.BAD_REQUEST
    EXPECTED_STATUS_EMPTY_EMAIL = HTTPStatus.BAD_REQUEST

    @allure.story("Негативные сценарии")
    @allure.title("Логин с неверным паролем")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_wrong_password(self, auth_service_anonym, registered_user):
        email = registered_user["email"]

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.login_user(
                LoginRequest(
                    email=email,
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
    def test_login_nonexistent_user(self, auth_service_anonym, test_user_credentials):
        email = self.NONEXISTENT_USER_EMAIL

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.login_user(
                LoginRequest(
                    email=email,
                    password=self.PASSWORD_NONEXISTENT_USER
                )
            )
        actual_status = exc_info.value.status_code
        assert actual_status == self.EXPECTED_STATUS_NONEXISTENT_USER, \
            f"Expected: {self.EXPECTED_STATUS_NONEXISTENT_USER}\n" \
            f"Actual: {actual_status}"

    @allure.story("Негативные сценарии")
    @allure.title("Логин с пустым email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_empty_email(self, auth_service_anonym):
        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.login_user_raw(
                LoginRequestRaw(
                    email="",
                    password="any_password"
                )
            )
        actual_status = exc_info.value.status_code
        assert actual_status == self.EXPECTED_STATUS_EMPTY_EMAIL, f"Expected: {self.EXPECTED_STATUS_EMPTY_EMAIL}\n" \
                                                                  f"Actual: {actual_status}"

    @allure.story("Негативные сценарии")
    @allure.title("Логин с пустым паролем")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_empty_password(self, auth_service_anonym, test_user_credentials):
        email = test_user_credentials["email"]

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.login_user_raw(
                LoginRequestRaw(
                    email=email,
                    password=""
                )
            )
        actual_status = exc_info.value.status_code
        assert actual_status == self.EXPECTED_STATUS_EMPTY_PASSWORD
