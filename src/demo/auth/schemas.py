from pydantic import BaseModel


class AuthAccount(BaseModel):
    id: int
    email: str
    username: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
