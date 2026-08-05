from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel


class BaseUser(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        alias_generator=to_camel,
        populate_by_name=True
    )

    email: EmailStr
    full_name: str
