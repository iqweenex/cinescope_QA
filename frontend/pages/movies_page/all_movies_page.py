from playwright.sync_api import Page
from .base_movies_page import BaseMoviesPage
from frontend.elements.button import Button
from frontend.elements.web_element import WebElement
from frontend.elements.label import Label


class AllMoviesPage(BaseMoviesPage):
    UNIQUE_ELEMENT_LOC = "//*[contains(@data-qa-id, 'movies_filter_location_select')]"
    MOVIES_FILTER_LOCATION_LOCATOR = "//*[contains(@data-qa-id, 'movies_filter_location_select')]"
    MOVIES_FILTER_GENRE_LOCATOR = "Пока нету"
    MOVIES_SORTER_CREATED_AT_LOCATOR = "//*[contains(@data-qa-id, 'movies_filter_created_at_select')]"

    NEXT_PAGE_BUTTON_LOCATOR = "//*[contains(@aria-label, 'Go to next')]"
    PREV_PAGE_BUTTON_LOCATOR = "//*[contains(@aria-label, 'Go to previous')]"
    _NUMBER_OF_PAGE_LOCATOR = "//*[contains(@href, 'movies?page')]" # Но ПОКА ХЗ!!!

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_name = "All movies catalogue page with pagination"
        self.unique_element = WebElement(page, self.UNIQUE_ELEMENT_LOC, "Уникальный элемент страницы всех фильмов")

        self.next_page_button = Button(page, self.NEXT_PAGE_BUTTON_LOCATOR, "Кнопка пагинации 'Вперед'")
        self.prev_page_button = Button(page, self.PREV_PAGE_BUTTON_LOCATOR, "Кнопка пагинации 'Назад'")
