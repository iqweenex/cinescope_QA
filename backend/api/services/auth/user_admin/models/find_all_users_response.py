from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from backend.api.services.auth.user_admin.models.admin_user_response import UserResponse


class FindAllUsersResponse(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        alias_generator=to_camel,
        populate_by_name=True
    )

    users: list[UserResponse]
    count: int
    page: int
    page_size: int
