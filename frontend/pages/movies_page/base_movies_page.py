from playwright.sync_api import Page
from frontend.pages.base_page import BasePage
from frontend.elements.button import Button


class BaseMoviesPage(BasePage):
    UNIQUE_ELEMENT_LOC = None
    PROFILE_PAGE_BUTTON_LOCATOR = "//*[contains(@data-qa-id, 'profile_page_button')]"
    LOGIN_BUTTON_LOCATOR = "//*[contains(@data-qa-id, 'login_page_button')]"
    ALL_MOVIES_BUTTON_LOCATOR = "//a[contains(@href, 'movies?page')]"

    def __init__(self, page: Page):
        super().__init__(page)
        self.all_movies_link = Button(page, self.ALL_MOVIES_BUTTON_LOCATOR, "Ссылка 'Все фильмы'")
        self.profile_button = Button(page, self.PROFILE_PAGE_BUTTON_LOCATOR, "Кнопка 'Профиль'")
        self.login_header_button = Button(page, self.LOGIN_BUTTON_LOCATOR, "Кнопка 'Войти' в шапке")

    def click_all_movies(self) -> None:
        self.all_movies_link.click()

    def is_user_logged_in(self) -> bool:
        return self.profile_button.is_visible()

    def is_user_logged_out(self) -> bool:
        return self.login_header_button.is_visible()
