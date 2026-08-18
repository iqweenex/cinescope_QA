from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class RegisterRequestRaw(BaseModel):
    """
    Модель для негативных тестов. Без валидации полей.
    Используется только для проверки реакции сервера на невалидные данные.
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="allow"
    )

    email: str
    full_name: str
    password: str
    password_repeat: str
