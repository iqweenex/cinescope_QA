import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_UI_URL = os.getenv("BASE_UI_URL", "https://dev-cinescope.t-qa.ru")
    AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "https://auth.dev-cinescope.t-qa.ru")
    MOVIES_SERVICE_URL = os.getenv("MOVIES_SERVICE_URL", "https://api.dev-cinescope.t-qa.ru")
    PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL", "https://payment.dev-cinescope.t-qa.ru")

    BASIC_AUTH_USER = os.getenv("BASIC_AUTH_USER", "admin")
    BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD", "admin")

    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL")
    TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")
    TEST_USER_FULL_NAME = os.getenv("TEST_USER_FULL_NAME", "Test User")

    DB_HOST = os.getenv("DB_HOST", "147.45.143.178")
    DB_PORT = os.getenv("DB_PORT", "31200")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME", "cinescope_db")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    TEST_CARD_NUMBER = os.getenv("TEST_CARD_NUMBER")
    TEST_CARD_EXPIRY = os.getenv("TEST_CARD_EXPIRY")
    TEST_CARD_CVV = os.getenv("TEST_CARD_CVV")