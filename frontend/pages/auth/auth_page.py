from playwright.sync_api import Page
from frontend.pages.base_page import BasePage
from frontend.elements.base_element import BaseElement as Label


class AuthPage(BasePage):
    UNIQUE_ELEMENT_LOC = "//a[contains(@href, 'register')]"
    SUCCESS_MESSAGE_LOC = "//div[contains(@role, 'status')]"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_name = "basic Auth page"
        self.unique_element = Label(page, self.UNIQUE_ELEMENT_LOC, "Сообщение об успешной авторизации")
        self.success_message = Label(page, self.SUCCESS_MESSAGE_LOC, "Сообщение об успешной авторизации")

    def get_success_message(self) -> str:
        return self.success_message.get_text()
