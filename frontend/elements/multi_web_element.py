from playwright.sync_api import Page, Locator
from .web_element import WebElement


class MultiWebElement:
    def __init__(self,
                 page: Page,
                 locator: str,
                 description: str = None) -> None:
        self.page = page
        self.index = 0

        self.selector = f"xpath={locator}" if '/' in locator else f"id={locator}"
        self.description = description if description else locator
        self.root_locator: Locator = self.page.locator(self.selector)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self) -> WebElement:
        if self.index >= self.root_locator.count():
            raise StopIteration
        current_element = self.get_by_index(self.index)
        self.index += 1
        return current_element

    def __len__(self) -> int:
        return self.root_locator.count()

    def get_by_index(self, index: int) -> WebElement:
        nth_locator = self.root_locator.nth(index)
        element = WebElement(self.page, self.selector, f"{self.description}[{index}]")
        element.locator = nth_locator
        return element
