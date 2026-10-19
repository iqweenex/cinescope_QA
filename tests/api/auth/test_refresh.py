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

        soft_assert.assert_true("accessToken" in response, "Ответ должен содержать accessToken")
        soft_assert.assert_true(response["accessToken"] is not None, "accessToken не должен быть None")
        soft_assert.assert_true("expiresIn" in response, "Ответ должен содержать expiresIn")


@allure.epic("Auth API")
@allure.feature("Refresh токенов")
class TestRefreshNegative:
    REFRESH_WITHOUT_TOKEN_STATUS_CODE = HTTPStatus.UNAUTHORIZED
    REFRESH_INVALID_TOKEN_STATUS_CODE = HTTPStatus.UNAUTHORIZED

    @allure.story("Негативные сценарии")
    @allure.title("Обновление без refresh-токена")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_refresh_without_token(self, auth_service_factory):
        auth_service = auth_service_factory()

        with pytest.raises(ApiError) as exc_info:
            auth_service.refresh_tokens()

        assert exc_info.value.status_code == self.REFRESH_WITHOUT_TOKEN_STATUS_CODE, \
            f"Actual: {exc_info.value.status_code}\n" \
            f"Expected: {self.REFRESH_WITHOUT_TOKEN_STATUS_CODE}"

    @allure.story("Негативные сценарии")
    @allure.title("Обновление с невалидным refresh-токеном")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_refresh_invalid_token(self, auth_service_factory):
        auth_service = auth_service_factory(refresh_token=uuid.uuid4().hex)

        with pytest.raises(ApiError) as exc_info:
            auth_service.refresh_tokens()

        assert exc_info.value.status_code == self.REFRESH_INVALID_TOKEN_STATUS_CODE, \
            f"Actual: {exc_info.value.status_code}\n" \
            f"Expected: {self.REFRESH_INVALID_TOKEN_STATUS_CODE}"