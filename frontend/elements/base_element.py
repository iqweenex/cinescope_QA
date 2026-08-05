from playwright.sync_api import Page, Locator, TimeoutError, Error
from logger.logger import Logger


class BaseElement:
    DEFAULT_TIMEOUT = 5000

    def __init__(self,
                 page: Page,
                 locator: str,
                 description: str = None):
        self.page = page

        if '/' in locator:
            self.selector = f"xpath={locator}"
        else:
            self.selector = f"id={locator}"

        self.description = description if description else locator
        self.locator: Locator = self.page.locator(self.selector)

    def __str__(self):
        return f"Element '{self.description}' [{self.selector}]"

    def is_exist(self, timeout: int = DEFAULT_TIMEOUT) -> bool:
        Logger.info(f"{self}: wait for presence")
        try:
            self.locator.wait_for(state="attached", timeout=timeout)
            return True
        except TimeoutError as err:
            Logger.error(f"{self}: {err}")
            return False

    def is_visible(self, timeout: int = DEFAULT_TIMEOUT) -> bool:
        Logger.info(f"{self}: wait for visible")
        try:
            self.locator.wait_for(state="visible", timeout=timeout)
            return True
        except TimeoutError as err:
            Logger.error(f"{self}: {err}")
            return False

    def click(self) -> None:
        Logger.info(f"{self}: click")
        try:
            self.locator.click()
        except TimeoutError as err:
            Logger.error(f"{self}: Timeout waiting to click - {err}")
            raise

    def js_click(self) -> None:
        Logger.info(f"{self}: js_click")
        self.locator.click(force=True)

    def scroll_to_view(self) -> None:
        Logger.info(f"{self}: scrolling to view")
        self.locator.scroll_into_view_if_needed()

    def get_text(self) -> str:
        Logger.info(f"{self}: get text")
        text = self.locator.inner_text()
        Logger.info(f"{self}: text = {text}")
        return text

    def get_attribute(self, name: str) -> str:
        Logger.info(f"{self}: get attribute '{name}'")
        value = self.locator.get_attribute(name)
        Logger.info(f"{self}: attribute name='{name}', value='{value}'")
        return value if value is not None else ""
