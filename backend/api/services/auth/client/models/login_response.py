from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel


class UserInfo(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        alias_generator=to_camel,
        populate_by_name=True
    )

    id: str
    email: EmailStr
    full_name: str
    roles: list[str]


class LoginResponse(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        alias_generator=to_camel,
        populate_by_name=True
    )

    user: UserInfo
    access_token: str
    refresh_token: str
    expires_in: int
