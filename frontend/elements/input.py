from playwright.sync_api import TimeoutError, Error
from logger.logger import Logger
from .base_element import BaseElement


class Input(BaseElement):
    def clear(self) -> None:
        Logger.info(f"{self}: clear")
        try:
            self.locator.clear()
        except TimeoutError as err:
            Logger.error(f"{self}: Timeout waiting to clear input: {err}")
            raise
        except Error as err:
            Logger.error(f"{self}: Clear failed: {err}")
            raise

    def js_clear(self) -> None:
        Logger.info(f"{self}: js clear")
        try:
            self.locator.fill("", force=True)
        except Error as err:
            Logger.error(f"{self}: JS clear failed: {err}")
            raise

    def send_keys(self, keys: str, clear: bool = True) -> None:
        if clear:
            self.clear()

        Logger.info(f"{self}: send keys = '{keys}'")
        try:
            if clear:
                self.locator.fill(keys)
            else:
                self.locator.press_sequentially(keys)
        except TimeoutError as err:
            Logger.error(f"{self}: Timeout waiting to send keys: {err}")
            raise
        except Error as err:
            Logger.error(f"{self}: Send keys failed: {err}")
            raise

    def js_send_keys(self, keys: str, clear: bool = True) -> None:
        if clear:
            self.js_clear()

        Logger.info(f"{self}: js send keys = '{keys}'")
        try:
            self.locator.evaluate(f"(el) => el.value = '{keys}'")
        except Error as err:
            Logger.error(f"{self}: JS send keys failed: {err}")
            raise
