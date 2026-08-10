from playwright.sync_api import Page
from .base_movies_page import BaseMoviesPage
from frontend.elements.button import Button
from frontend.elements.input import Input
from frontend.elements.label import Label
from frontend.elements.web_element import WebElement
from logger.logger import Logger


class MoviePage(BaseMoviesPage):
    UNIQUE_ELEMENT_LOC = "//*[contains(@class, 'lucide-shopping-cart')]"
    BUY_TICKET_BUTTON_LOCATOR = "//*[contains(@class, 'lucide-shopping-cart')]"
    REVIEW_TEXT_INPUT_LOCATOR = "//*[contains(@data-qa-id, 'movie_review_input')]"
    RATING_SELECT_LOCATOR = "//*[contains(@role, 'combobox')]"
    SUBMIT_REVIEW_BUTTON_LOCATOR = "//*[contains(@type, 'submit')]"
    RATING_LISTBOX_LOCATOR = "//*[contains(@id, 'radix-') and @role='listbox']"

    _RATING_OPTION_TEMPLATE = "//*[contains(@id, 'radix-') and @role='listbox']//*[@role='option' and .//text()='{}']"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_name = "Movie Details Page"
        self.unique_element = Button(page, self.UNIQUE_ELEMENT_LOC, "Уникальный элемент страницы")
        self.buy_ticket_button = Button(page, self.BUY_TICKET_BUTTON_LOCATOR, "Кнопка 'Купить билет'")
        self.review_text_input = Input(page, self.REVIEW_TEXT_INPUT_LOCATOR, "Поле ввода отзыва")
        self.rating_select = Button(page, self.RATING_SELECT_LOCATOR, "Кнопка выпадающего списка оценки")
        self.submit_review_button = Button(page, self.SUBMIT_REVIEW_BUTTON_LOCATOR, "Кнопка 'Отправить отзыв'")
        self.rating_listbox = WebElement(page, self.RATING_LISTBOX_LOCATOR, "Листбокс с оценками")

    def is_buy_button_visible(self) -> bool:
        return self.buy_ticket_button.is_visible()

    def click_buy_ticket(self) -> None:
        self.buy_ticket_button.scroll_to_view()
        self.buy_ticket_button.click()

    def leave_review(self, text: str, score: str) -> None:
        Logger.info(f"{self}: Оставляем отзыв со скиллом '{score}'")

        self.review_text_input.send_keys(text)

        self.rating_select.click()

        option_xpath = self._RATING_OPTION_TEMPLATE.format(score)
        option_button = Button(self.page, option_xpath, f"Оценка '{score}' в выпадающем списке")
        option_button.click()

        self.submit_review_button.click()
