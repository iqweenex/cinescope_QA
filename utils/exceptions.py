# utils/exceptions.py
class ApiError(Exception):
    def __init__(self, status_code: int, messages: list):
        self.status_code = status_code
        self.messages = messages if isinstance(messages, list) else [messages]
        super().__init__(f"API Error {status_code}: {', '.join(self.messages)}")
