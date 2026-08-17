import pytest
import allure
from backend.api.services.auth.client.models.register_request import RegisterRequest


@allure.epic("Auth API")
@allure.feature("Регистрация")
class TestRegister:

    @allure.story("Позитивные сценарии")
    @allure.title("Успешная регистрация нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_register_success(self, auth_service_anonym, test_user_credentials, soft_assert):
        email = test_user_credentials["email"]
        password = test_user_credentials["password"]
        full_name = test_user_credentials["full_name"]

        response = auth_service_anonym.register_user(
            RegisterRequest(
                email=email,
                full_name=full_name,
                password=password,
                password_repeat=password
            )
        )

        soft_assert.assert_true(bool(response.id), "id должен быть заполнен")
        soft_assert.assert_equal(response.email, email, "email не совпадает")
        soft_assert.assert_equal(response.full_name, full_name, "full_name не совпадает")
        soft_assert.assert_true(not response.verified, "verified должен быть False")
        soft_assert.assert_true(not response.banned, "banned должен быть False")
        soft_assert.assert_true("password" not in response.model_dump(), "пароль не должен возвращаться в ответе")

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с дублирующимся email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_register_duplicate_email(self, auth_service_anonym, registered_user):
        email = registered_user["email"]
        password = registered_user["password"]
        full_name = registered_user["full_name"]

        with pytest.raises(Exception) as exc_info:
            auth_service_anonym.register_user(
                RegisterRequest(
                    email=email,
                    full_name=full_name,
                    password=password,
                    password_repeat=password
                )
            )

        assert "409" in str(exc_info.value) or "Conflict" in str(exc_info.value)
