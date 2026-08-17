from logger.logger import Logger


class SoftAssert:
    """
    Custom soft-assert
    """

    def __init__(self):
        self._errors = []

    def assert_equal(self, actual, expected, message: str = None):
        Logger.info("Soft assert equal")
        if actual != expected:
            error_msg = message or f"Expected: {expected}" \
                                   f"Actual: {actual}"
            self._errors.append(error_msg)
        return actual == expected

    def assert_true(self, condition, message: str = None):
        Logger.info("Soft assert condition")
        if not condition:
            error_msg = message or f"{condition} = False"
            self._errors.append(error_msg)
        return condition

    def assert_all(self):
        if self._errors:
            error_messages = "\n".join(self._errors)
            self._errors.clear()
            raise AssertionError(f"Soft assert failed: \n"
                                 f"{error_messages}")

    def get_errors(self):
        return self._errors.copy()

    def clear(self):
        self._errors.clear()
