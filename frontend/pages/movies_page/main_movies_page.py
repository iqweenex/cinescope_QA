from playwright.sync_api import Page
from frontend.pages.base_page import BasePage
from frontend.elements.button import Button
from frontend.elements.web_element import WebElement
from frontend.elements.multi_web_element import MultiWebElement
from .base_movies_page import BaseMoviesPage
from frontend.elements.label import Label
from logger.logger import Logger
from config import Config


class MainPage(BaseMoviesPage):
    UNIQUE_ELEMENT_LOC = "//h2[contains(@class, 'text-4xl') and text()='Последние фильмы']"
    TITLE_MAIN_PAGE_LOCATOR = "//h2[contains(@class, 'text-4xl') and text()='Последние фильмы']"
    SHOW_MORE_MOVIES_BUTTON = "//*[contains(@class, 'w-full mt-10 flex justify-end')]//*[contains(@href, 'movies')]"

    _MOVIE_CARDS_LOCATOR = "//div[contains(@class, 'rounded-xl border bg-card')]"
    _MOVIE_TITLE_BY_INDEX_TEMPLATE = "(//div[contains(@class, 'rounded-xl border bg-card')])[{}]//h3"
    _MORE_BUTTON_BY_INDEX_TEMPLATE = "(//div[contains(@class, 'rounded-xl border bg-card')])[{}]" \
                                     "//*[contains(@data-qa-id, 'more_button')]"

    _SPECIFIC_MOVIE_BY_NAME_TEMPLATE = "//div[contains(@class, 'rounded-xl border bg-card')]" \
                                       "[.//h3[text()='{}']]//*[contains(@data-qa-id, 'more_button')]"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_name = "Main movies catalogue page"

        self.unique_element = WebElement(page, self.UNIQUE_ELEMENT_LOC, "Уникальный элемент")
        self.title_main_movies_page = Label(page, self.TITLE_MAIN_PAGE_LOCATOR, "Заголовок 'Последние фильмы'")
        self.movie_cards = MultiWebElement(page, self._MOVIE_CARDS_LOCATOR, "Коллекция карточек фильмов")
        self.show_more_movies_button = Button(page, self.SHOW_MORE_MOVIES_BUTTON, "Кнопка показать больше")

    def get_movies_count(self) -> int:
        count = len(self.movie_cards)
        Logger.info(f"Найдено {count} фильмов на главной странице")
        return count

    def click_movie_details_by_index(self, movie_index: int) -> None:
        xpath_index = movie_index + 1
        btn_xpath = self._MORE_BUTTON_BY_INDEX_TEMPLATE.format(xpath_index)

        details_button = Button(self.page, btn_xpath, f"Кнопка 'Подробнее' фильма №{xpath_index}")

        details_button.scroll_to_view()
        details_button.click()

    def get_movie_title_by_index(self, movie_index: int) -> str:
        xpath_index = movie_index + 1
        title_xpath = self._MOVIE_TITLE_BY_INDEX_TEMPLATE.format(xpath_index)

        title_element = WebElement(self.page, title_xpath, f"Название фильма №{xpath_index}")
        return title_element.get_text()

    def click_movie_details_by_name(self, movie_name: str) -> None:
        specific_btn_xpath = self._SPECIFIC_MOVIE_BY_NAME_TEMPLATE.format(movie_name)

        details_button = Button(self.page, specific_btn_xpath, f"Кнопка 'Подробнее' для фильма '{movie_name}'")
        details_button.scroll_to_view()
        details_button.click()
