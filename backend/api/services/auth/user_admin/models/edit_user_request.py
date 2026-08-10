from pydantic import BaseModel, ConfigDict


class EditUserRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')

    roles: list[str]
    verified: bool
    banned: bool
