from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel


class UserInfo(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        alias_generator=to_camel,
        populate_by_name=True
    )

    id: str
    login: str
    email: EmailStr | None = None
    full_name: str
    created_at: str
    verified: bool
    banned: bool
    roles: list[str]


class LoginResponse(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        alias_generator=to_camel,
        populate_by_name=True
    )

    user: UserInfo
    access_token: str
    expires_in: int
