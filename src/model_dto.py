from pydantic import BaseModel, EmailStr, constr


class LoginDto(BaseModel):
    username: str
    password: str


class userDto(BaseModel):
    username: constr(min_length=1)
    password: constr(min_length=1)
    email: EmailStr
    mobile_nr: str
    role: constr(min_length=1)
