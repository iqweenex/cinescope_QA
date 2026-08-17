import time
import pytest
import requests
from playwright.sync_api import sync_playwright, Playwright
from logger.logger import Logger
from backend.api.services.auth.auth_service import AuthService


def wait_for_service(url: str, name_service: str, timeout: int = 180, interval: int = 2):
    Logger.info(f"Waiting for '{name_service}' during '{timeout}' seconds")
    start_time = time.time()
    while time.time() < start_time + timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code < 500:
                break
        except requests.exceptions.RequestException:
            time.sleep(interval)
    else:
        raise RuntimeError(f"{name_service} wasn't started during '{timeout}' seconds")


@pytest.fixture(scope='session', autouse=True)
def services_readiness():
    wait_for_service(f"{AuthService.SERVICE_URL}/swagger", "Auth Microservice")
    yield


@pytest.fixture(scope="session")
def playwright_launcher() -> Playwright:
    Logger.info("Инициализация глобального движка Playwright")
    with sync_playwright() as playwright:
        yield playwright
    Logger.info("Завершение работы глобального движка Playwright")
