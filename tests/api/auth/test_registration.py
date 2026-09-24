import pytest
import allure
from backend.api.services.auth.client.models.register_request import RegisterRequest
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
    def test_register_success(self, auth_service_anonym, user_data_factory, soft_assert):
        data = user_data_factory()

        Logger.info(f"Регистрация пользователя: email={data['email']}, login={data['login']}")

        response = auth_service_anonym.register_user(
            RegisterRequest(
                login=data["login"],
                email=data["email"],
                password=data["password"]
            )
        )

        Logger.info(f"Создан пользователь:\n "
                    f"id={response.id}\n"
                    f"email={response.email}\n"
                    f"login={response.login}")

        soft_assert.assert_true(bool(response.id), "id должен быть заполнен")
        soft_assert.assert_equal(response.login, data["login"], "login не совпадает")
        soft_assert.assert_equal(response.email, data["email"], "email не совпадает")
        soft_assert.assert_equal(response.full_name, data["login"], "fullName должен быть равен login")
        soft_assert.assert_true(response.verified, "verified должен быть True")
        soft_assert.assert_true(not response.banned, "banned должен быть False")
        soft_assert.assert_true("password" not in response.model_dump(), "пароль не должен возвращаться")


@allure.epic("Auth API")
@allure.feature("Регистрация")
class TestRegisterNegative:
    DUPLICATE_MAIL_ERROR_MESSAGE = "Пользователь с таким email уже зарегистрирован"
    DUPLICATE_LOGIN_ERROR_MESSAGE = "Пользователь с таким login уже зарегистрирован"
    INVALID_MAIL_ERROR_MESSAGE = "Некорректный email"
    EMPTY_FIELDS_ERROR_MESSAGE = "не должно быть пустым"
    PASSWORD_TOO_SHORT_MESSAGE = "Минимальная длина пароля 8 символов"
    PASSWORD_NO_UPPERCASE_MESSAGE = "Пароль должен содержать хотя бы одну заглавную букву"
    PASSWORD_NO_DIGITS_ERROR_MESSAGE = "Пароль должен содержать хотя бы одну цифру"

    DUPLICATE_MAIL_OR_LOGIN_STATUS_CODE = HTTPStatus.CONFLICT
    INVALID_MAIL_STATUS_CODE = HTTPStatus.BAD_REQUEST
    EMPTY_FIELD_STATUS_CODE = HTTPStatus.BAD_REQUEST
    PASSWORD_TOO_SHORT_STATUS_CODE = HTTPStatus.BAD_REQUEST
    PASSWORD_NO_UPPERCASE_STATUS_CODE = HTTPStatus.BAD_REQUEST
    PASSWORD_NO_DIGITS_STATUS_CODE = HTTPStatus.BAD_REQUEST

    TEST_PASSWORD_TOO_SHORT = "Abcd1"
    TEST_PASSWORD_NO_UPPERCASE = "abcd123456"
    TEST_PASSWORD_NO_DIGITS = "Abcdesgdgsdg"
    TEST_INVALID_MAIL = "email"

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с дублирующимся email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_register_duplicate_email(self, auth_service_anonym, registered_user, user_data_factory):
        data = user_data_factory(email=registered_user["email"])

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.register_user(
                RegisterRequest(
                    login=data["login"],
                    email=data["email"],
                    password=data["password"]
                )
            )

        assert exc_info.value.status_code == self.DUPLICATE_MAIL_OR_LOGIN_STATUS_CODE, (
            f"Expected status code: {self.DUPLICATE_MAIL_OR_LOGIN_STATUS_CODE}\n"
            f"Actual status code: {exc_info.value.status_code}"
        )

        assert self.DUPLICATE_MAIL_ERROR_MESSAGE in exc_info.value.messages, (
            f"Expected error message: {self.DUPLICATE_MAIL_ERROR_MESSAGE}\n"
            f"Actual message: {exc_info.value.messages}"
        )

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с дублирующимся login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_register_duplicate_login(self, auth_service_anonym, registered_user, user_data_factory):
        data = user_data_factory(login=registered_user["login"])

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.register_user(
                RegisterRequest(
                    login=data["login"],
                    email=data["email"],
                    password=data["password"]
                )
            )

        assert exc_info.value.status_code == self.DUPLICATE_MAIL_OR_LOGIN_STATUS_CODE, (
            f"Expected status code: {self.DUPLICATE_MAIL_OR_LOGIN_STATUS_CODE}\n"
            f"Actual status code: {exc_info.value.status_code}"
        )

        assert self.DUPLICATE_LOGIN_ERROR_MESSAGE in exc_info.value.messages, (
            f"Expected error message: {self.DUPLICATE_LOGIN_ERROR_MESSAGE}\n"
            f"Actual message: {exc_info.value.messages}"
        )

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с невалидным email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_register_invalid_email(self, auth_service_anonym, user_data_factory):
        """
        Проверяем, что сервер возвращает 400 при отправке невалидного email.
        """
        data = user_data_factory(email=self.TEST_INVALID_MAIL)

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.register_user_raw(
                data={
                    "login": data["login"],
                    "email": data["email"],
                    "password": data["password"]
                }
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
    @allure.title("Регистрация с пустыми полями")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_register_empty_fields(self, auth_service_anonym, user_data_factory):
        data = user_data_factory(login="", email="", password="")

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.register_user_raw(
                data={
                    "login": data["login"],
                    "email": data["email"],
                    "password": data["password"]
                }
            )

        assert exc_info.value.status_code == self.INVALID_MAIL_STATUS_CODE, (
            f"Expected status code: {self.INVALID_MAIL_STATUS_CODE}\n"
            f"Actual status code: {exc_info.value.status_code}"
        )

        assert any("login" in msg.lower() or "пароль" in msg.lower()
                   for msg in exc_info.value.messages), (
            f"Expected messages about login or password\n"
            f"Actual messages: {exc_info.value.messages}"
        )

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с паролем менее 8 символов")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_register_password_too_short(self, auth_service_anonym, user_data_factory):
        data = user_data_factory(password=self.TEST_PASSWORD_TOO_SHORT)

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.register_user(
                RegisterRequest(
                    login=data["login"],
                    email=data["email"],
                    password=data["password"]
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
    def test_register_password_no_uppercase(self, auth_service_anonym, user_data_factory):
        data = user_data_factory(password=self.TEST_PASSWORD_NO_UPPERCASE)

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.register_user(
                RegisterRequest(
                    login=data["login"],
                    email=data["email"],
                    password=data["password"]
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
    def test_register_password_no_digits(self, auth_service_anonym, user_data_factory):
        data = user_data_factory(password=self.TEST_PASSWORD_NO_DIGITS)

        with pytest.raises(ApiError) as exc_info:
            auth_service_anonym.register_user(
                RegisterRequest(
                    login=data["login"],
                    email=data["email"],
                    password=data["password"]
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
