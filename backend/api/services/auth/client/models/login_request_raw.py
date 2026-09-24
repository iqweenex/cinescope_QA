from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class LoginRequestRaw(BaseModel):
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
    password: str