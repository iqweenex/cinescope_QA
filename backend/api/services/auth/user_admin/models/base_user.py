from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel


class BaseUser(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        alias_generator=to_camel,
        populate_by_name=True
    )

    login: str
    email: EmailStr | None = None
    full_name: str
