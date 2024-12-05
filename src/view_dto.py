from pydantic import BaseModel


class RegisterDto(BaseModel):
    username: str
    password: str
    email: str
    mobile_nr: str


class LoginDto(BaseModel):
    username: str
    password: str
