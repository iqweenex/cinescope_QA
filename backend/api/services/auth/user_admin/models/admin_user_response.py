from backend.api.services.auth.user_admin.models.base_user import BaseUser


class UserResponse(BaseUser):
    id: str
    roles: list[str]
    verified: bool
    created_at: str
    banned: bool
