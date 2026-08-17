from backend.api.services.auth.user_admin.models.base_user import BaseUser


class CreateUserRequest(BaseUser):
    password: str
    verified: bool
    banned: bool
