from pydantic import BaseModel


class Session(BaseModel):
    sub: str
    token: str
    iat: int
    exp: int
