from pydantic import BaseModel


class Session(BaseModel):
    user_id: str
    access_token: str
    issued_at: int
    expires_at: int
