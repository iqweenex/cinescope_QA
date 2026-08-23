import pytest
import allure
import requests
from backend.api.services.auth.client.models.register_request import RegisterRequest
from backend.api.services.auth.client.models.register_request_raw import RegisterRequestRaw
from logger.logger import Logger
from utils.exceptions import ApiError
from utils.constants import HTTPStatus


@allure.epic("Auth API")
@allure.feature("Регистрация")
class TestRegisterPositive:
    @allure.story("Позитивные сценарии")
    @allure.title("Успешная регистрация нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_register_success(self, auth_service_anonym, test_user_credentials, soft_assert):
        email = test_user_credentials["email"]
        password = test_user_credentials["password"]
        full_name = test_user_credentials["full_name"]

        Logger.info(f"Регистрация пользователя: email={email}, full_name={full_name}")

        response = auth_service_anonym.register_user(
            RegisterRequest(
                email=email,
                full_name=full_name,
                password=password,
                password_repeat=password
            )
        )

        Logger.info(f"Создан пользователь: id={response.id}\n"
                    f"email={response.email}\n"
                    f"full_name={response.full_name}")

        soft_assert.assert_true(bool(response.id), "id должен быть заполнен")
        soft_assert.assert_equal(response.email, email, "email не совпадает")
        soft_assert.assert_equal(response.full_name, full_name, "full_name не совпадает")
        soft_assert.assert_true(response.verified, "verified должен быть True")
        soft_assert.assert_true(not response.banned, "banned должен быть False")
        soft_assert.assert_true("password" not in response.model_dump(), "пароль не должен возвращаться в ответе")


@allure.epic("Auth API")
@allure.feature("Регистрация")
class TestRegisterNegative:
    DUPLICATE_MAIL_ERROR_MESSAGE = "Пользователь с таким email уже зарегистрирован"
    INVALID_MAIL_ERROR_MESSAGE = "Некорректный email"
    MISSMATCH_PASSWORDS_ERROR_MESSAGE = "Пароли не совпадают"
    EMPTY_FIELDS_ERROR_MESSAGE = "не должно быть пустым"
    PASSWORD_TOO_SHORT_MESSAGE = "Минимальная длина пароля 8 символов"
    PASSWORD_NO_UPPERCASE_MESSAGE = "Пароль должен содержать хотя бы одну заглавную букву"
    PASSWORD_NO_DIGITS_ERROR_MESSAGE = "Пароль должен содержать хотя бы одну цифру"

    DUPLICATE_MAIL_STATUS_CODE = HTTPStatus.CONFLICT
    INVALID_MAIL_STATUS_CODE = HTTPStatus.BAD_REQUEST
    MISSMATCH_PASSWORDS_STATUS_CODE = HTTPStatus.BAD_REQUEST
    EMPTY_FIELD_STATUS_CODE = HTTPStatus.BAD_REQUEST
    PASSWORD_TOO_SHORT_STATUS_CODE = HTTPStatus.BAD_REQUEST
    PASSWORD_NO_UPPERCASE_STATUS_CODE = HTTPStatus.BAD_REQUEST
    PASSWORD_NO_DIGITS_STATUS_CODE = HTTPStatus.BAD_REQUEST

    TEST_PASSWORD_TOO_SHORT = "Abcd1"
    TEST_PASSWORD_NO_UPPERCASE = "abcd123456"
    TEST_PASSWORD_NO_DIGITS = "Abcdesgdgsdg"
    TEST_INVALID_MAIL = "testmail"

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с дублирующимся email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_register_duplicate_email(self, auth_service_anonym, registered_user):
        email = registered_user["email"]
        password = registered_user["password"]
        full_name = registered_user["full_name"]

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.register_user(
                RegisterRequest(
                    email=email,
                    full_name=full_name,
                    password=password,
                    password_repeat=password
                )
            )

        assert exc_info.value.status_code == self.DUPLICATE_MAIL_STATUS_CODE, (
            f"Expected status code: {self.DUPLICATE_MAIL_STATUS_CODE}\n"
            f"Actual status code: {exc_info.value.status_code}"
        )

        assert self.DUPLICATE_MAIL_ERROR_MESSAGE in exc_info.value.messages, (
            f"Expected error message: {self.DUPLICATE_MAIL_ERROR_MESSAGE}\n"
            f"Actual message: {exc_info.value.messages}"
        )

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с невалидным email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_register_invalid_email(self, auth_service_anonym, test_user_credentials):
        """
        Проверяем, что сервер возвращает 400 при отправке невалидного email.
        Используем RegisterRequestRaw, чтобы обойти Pydantic-валидацию.
        """
        password = test_user_credentials["password"]
        full_name = test_user_credentials["full_name"]

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.register_user_raw(
                RegisterRequestRaw(
                    email="invalid-email",
                    full_name=full_name,
                    password=password,
                    password_repeat=password
                )
            )

        assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST
        assert "Некорректный email" in exc_info.value.messages

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с несовпадающими паролями")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_register_password_mismatch(self, auth_service_anonym, test_user_credentials):
        email = test_user_credentials["email"]
        password = test_user_credentials["password"]
        full_name = test_user_credentials["full_name"]

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.register_user(
                RegisterRequest(
                    email=email,
                    full_name=full_name,
                    password=password,
                    password_repeat=password + "1"
                )
            )

        assert exc_info.value.status_code == self.MISSMATCH_PASSWORDS_STATUS_CODE, (
            f"Expected status code: {self.MISSMATCH_PASSWORDS_STATUS_CODE}\n"
            f"Actual status code: {exc_info.value.response.status_code}"
        )

        assert self.MISSMATCH_PASSWORDS_ERROR_MESSAGE in exc_info.value.messages, (
            f"Expected error message: {self.MISSMATCH_PASSWORDS_ERROR_MESSAGE}\n"
            f"Actual message: {exc_info.value.messages}"
        )

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с пустыми полями")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_register_empty_fields(self, auth_service_anonym, test_user_credentials):
        password = test_user_credentials["password"]
        full_name = test_user_credentials["full_name"]

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.register_user_raw(
                RegisterRequestRaw(
                    email=self.TEST_INVALID_MAIL,
                    full_name=full_name,
                    password=password,
                    password_repeat=password
                )
            )

        assert exc_info.value.status_code == self.INVALID_MAIL_STATUS_CODE, (
            f"Expected status code: {self.INVALID_MAIL_STATUS_CODE}\n"
            f"Actual status code: {exc_info.value.status_code}"
        )

        assert any(self.INVALID_MAIL_ERROR_MESSAGE in msg for msg in exc_info.value.messages), (
            f"Expected error message: {self.INVALID_MAIL_ERROR_MESSAGE}\n"
            f"Actual messages: {exc_info.value.messages}"
        )

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с паролем менее 8 символов")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_register_password_too_short(self, auth_service_anonym, test_user_credentials):
        email = test_user_credentials["email"]
        short_password = self.TEST_PASSWORD_TOO_SHORT
        full_name = test_user_credentials["full_name"]

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.register_user(
                RegisterRequest(
                    email=email,
                    full_name=full_name,
                    password=short_password,
                    password_repeat=short_password
                )
            )

        assert exc_info.value.status_code == self.PASSWORD_TOO_SHORT_STATUS_CODE, (
            f"Expected status code: {self.PASSWORD_TOO_SHORT_STATUS_CODE}\n"
            f"Actual status code: {exc_info.value.status_code}"
        )

        assert self.PASSWORD_TOO_SHORT_MESSAGE in exc_info.value.messages, (
            f"Expected error message: {self.PASSWORD_TOO_SHORT_MESSAGE}\n"
            f"Actual message: {exc_info.value.messages}"
        )

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с паролем без заглавной буквы")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_register_password_no_uppercase(self, auth_service_anonym, test_user_credentials):
        email = test_user_credentials["email"]
        full_name = test_user_credentials["full_name"]
        password_no_uppercase = self.TEST_PASSWORD_NO_UPPERCASE

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.register_user(
                RegisterRequest(
                    email=email,
                    full_name=full_name,
                    password=password_no_uppercase,
                    password_repeat=password_no_uppercase
                )
            )

        assert exc_info.value.status_code == self.PASSWORD_NO_UPPERCASE_STATUS_CODE, (
            f"Expected status code: {self.PASSWORD_NO_UPPERCASE_STATUS_CODE}\n"
            f"Actual status code: {exc_info.value.status_code}"
        )

        assert self.PASSWORD_NO_UPPERCASE_MESSAGE in exc_info.value.messages, (
            f"Expected error message: {self.PASSWORD_NO_UPPERCASE_MESSAGE}\n"
            f"Actual message: {exc_info.value.messages}"
        )

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с паролем без цифры")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_register_password_no_digits(self, auth_service_anonym, test_user_credentials):
        email = test_user_credentials["email"]
        full_name = test_user_credentials["full_name"]
        password_no_digits = self.TEST_PASSWORD_NO_DIGITS

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.register_user(
                RegisterRequest(
                    email=email,
                    full_name=full_name,
                    password=password_no_digits,
                    password_repeat=password_no_digits
                )
            )

        assert exc_info.value.status_code == self.PASSWORD_NO_DIGITS_STATUS_CODE, (
            f"Expected status code: {self.PASSWORD_NO_DIGITS_STATUS_CODE}\n"
            f"Actual status code: {exc_info.value.status_code}"
        )

        assert self.PASSWORD_NO_DIGITS_ERROR_MESSAGE in exc_info.value.messages, (
            f"Expected error message: {self.PASSWORD_NO_DIGITS_ERROR_MESSAGE}\n"
            f"Actual message: {exc_info.value.messages}"
        )
