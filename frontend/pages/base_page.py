from playwright.sync_api import Page
from logger.logger import Logger


class BasePage:
    UNIQUE_ELEMENT_LOC = None

    def __init__(self, page: Page):
        self.page = page
        self.page_name = None
        self.unique_element = None

    def __str__(self):
        return f"Page '{self.page_name}'"

    def wait_for_open(self) -> None:
        Logger.info(f"{self}: wait for open")
        if self.unique_element:
            is_opened = self.unique_element.is_exist()
            if not is_opened:
                raise RuntimeError(f"Page {self.page_name} was not opened (unique element not found)!")
        else:
            Logger.warning(f"{self}: UNIQUE_ELEMENT_LOC is not defined, skipping wait_for_open")
