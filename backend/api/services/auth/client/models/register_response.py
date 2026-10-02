from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel


class RegisterResponse(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        alias_generator=to_camel,
        populate_by_name=True
    )

    id: str
    login: str
    email: EmailStr | None = None
    full_name: str
    roles: list[str]
    verified: bool
    created_at: str
    banned: bool
