from pydantic import BaseModel


class SuccessResponse(BaseModel):
    status: str
    message: str | None = None
