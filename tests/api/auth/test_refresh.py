import pytest
import allure
from utils.exceptions import ApiError
from utils.constants import HTTPStatus
from utils.api_utils import ApiUtils
from config import Config
from backend.api.services.auth.auth_service import AuthService


@allure.epic("Auth API")
@allure.feature("Refresh токенов")
class TestRefreshPositive:
    """Позитивные сценарии обновления токенов"""

    @allure.story("Позитивные сценарии")
    @allure.title("Успешное обновление токенов")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_refresh_success(self, auth_service_with_refresh, soft_assert):
        response = auth_service_with_refresh.refresh_tokens()

        soft_assert.assert_true("accessToken" in response)
        soft_assert.assert_true("refreshToken" in response)
        soft_assert.assert_true(response["accessToken"] is not None)
        soft_assert.assert_true(response["refreshToken"] is not None)


@allure.epic("Auth API")
@allure.feature("Refresh токенов")
class TestRefreshNegative:
    """Негативные сценарии обновления токенов"""

    EXPECTED_STATUS_WITHOUT_TOKEN = HTTPStatus.UNAUTHORIZED
    EXPECTED_STATUS_INVALID_TOKEN = HTTPStatus.UNAUTHORIZED

    @allure.story("Негативные сценарии")
    @allure.title("Обновление без refresh-токена")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_refresh_without_token(self, auth_service_without_cookies):
        with pytest.raises(ApiError) as exc_info:
            auth_service_without_cookies.refresh_tokens()

        actual_status = exc_info.value.status_code
        assert actual_status == self.EXPECTED_STATUS_WITHOUT_TOKEN, \
            f"Expected: {self.EXPECTED_STATUS_WITHOUT_TOKEN}\n" \
            f"Actual: {actual_status}"

    @allure.story("Негативные сценарии")
    @allure.title("Обновление с невалидным refresh-токеном")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_refresh_invalid_token(self, auth_service_with_invalid_refresh):
        with pytest.raises(ApiError) as exc_info:
            auth_service_with_invalid_refresh.refresh_tokens()

        actual_status = exc_info.value.status_code
        assert actual_status == self.EXPECTED_STATUS_INVALID_TOKEN, \
            f"Expected: {self.EXPECTED_STATUS_INVALID_TOKEN}\n" \
            f"Actual: {actual_status}"
