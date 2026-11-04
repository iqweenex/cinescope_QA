import uuid
import pytest
import allure
from utils.exceptions import ApiError
from utils.constants import HTTPStatus

@allure.epic("Auth API")
@allure.feature("Refresh токенов")
class TestRefreshPositive:
    @allure.story("Позитивные сценарии")
    @allure.title("Успешное обновление токенов")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_refresh_success(self, auth_service_factory, logged_in_user, soft_assert):
        auth_service = auth_service_factory(refresh_token=logged_in_user["refresh_token"])
        response = auth_service.refresh_tokens()

        access_token = response.get("accessToken")
        expires_in = response.get("expiresIn")

        soft_assert.assert_true(isinstance(access_token, str) and len(access_token) > 0,
                                f"accessToken должен быть непустой строкой, получено: {access_token!r}")
        soft_assert.assert_true(isinstance(expires_in, int) and expires_in > 0,
                                f"accessToken должен быть непустой строкой, получено: {expires_in!r}")


@allure.epic("Auth API")
@allure.feature("Refresh токенов")
class TestRefreshNegative:
    REFRESH_WITHOUT_TOKEN_STATUS_CODE = HTTPStatus.UNAUTHORIZED
    REFRESH_INVALID_TOKEN_STATUS_CODE = HTTPStatus.UNAUTHORIZED
    UNAUTHORIZED_ERROR_MESSAGE = "Неверный токен"

    @allure.story("Негативные сценарии")
    @allure.title("Обновление без refresh-токена")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_refresh_without_token(self, auth_service_factory):
        auth_service = auth_service_factory()

        with pytest.raises(ApiError) as exc_info:
            auth_service.refresh_tokens()

        assert exc_info.value.status_code == self.REFRESH_WITHOUT_TOKEN_STATUS_CODE, (
            f"Expected: {self.REFRESH_WITHOUT_TOKEN_STATUS_CODE}\n"
            f"Actual: {exc_info.value.status_code}"
        )
        assert any(self.UNAUTHORIZED_ERROR_MESSAGE in msg for msg in exc_info.value.messages), (
            f"Expected message: {self.UNAUTHORIZED_ERROR_MESSAGE}\n"
            f"Actual messages: {exc_info.value.messages}"
        )

    @allure.story("Негативные сценарии")
    @allure.title("Обновление с невалидным refresh-токеном")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_refresh_invalid_token(self, auth_service_factory):
        auth_service = auth_service_factory(refresh_token=uuid.uuid4().hex)

        with pytest.raises(ApiError) as exc_info:
            auth_service.refresh_tokens()

        assert exc_info.value.status_code == self.REFRESH_INVALID_TOKEN_STATUS_CODE, (
            f"Expected: {self.REFRESH_INVALID_TOKEN_STATUS_CODE}\n"
            f"Actual: {exc_info.value.status_code}"
        )
        assert any(self.UNAUTHORIZED_ERROR_MESSAGE in msg for msg in exc_info.value.messages), (
            f"Expected message: {self.UNAUTHORIZED_ERROR_MESSAGE}\n"
            f"Actual messages: {exc_info.value.messages}"
        )