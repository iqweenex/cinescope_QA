import pytest
from playwright.sync_api import Playwright, Browser, BrowserContext, Page
from logger.logger import Logger
from config import Config
from frontend.pages.auth.auth_page import AuthPage
from frontend.pages.movies_page.main_movies_page import MainPage
from frontend.pages.movies_page.movie_page import MoviePage


@pytest.fixture(scope="session")
def browser(playwright_launcher: Playwright) -> Browser:
    Logger.info("Запуск браузера Chromium")
    browser_instance = playwright_launcher.chromium.launch(headless=False)
    yield browser_instance
    Logger.info("Закрытие браузера Chromium")
    browser_instance.close()


@pytest.fixture(scope="function")
def browser_context(browser: Browser) -> BrowserContext:
    Logger.info("Создание нового контекста браузера с поддержкой Basic Auth")

    context = browser.new_context(
        http_credentials={
            "username": Config.BASIC_AUTH_USER,
            "password": Config.BASIC_AUTH_PASSWORD
        }
    )

    context.set_default_timeout(10000)
    yield context
    Logger.info("Закрытие контекста браузера")
    context.close()


@pytest.fixture(scope="function")
def ui_page(browser_context: BrowserContext) -> Page:
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def auth_page(ui_page: Page) -> AuthPage:
    return AuthPage(page=ui_page)


@pytest.fixture(scope="function")
def main_page(ui_page: Page) -> MainPage:
    return MainPage(page=ui_page)


@pytest.fixture(scope="function")
def movie_page(ui_page: Page) -> MoviePage:
    return MoviePage(page=ui_page)
