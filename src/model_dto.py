from pydantic import BaseModel, EmailStr, constr


class RegisterDto(BaseModel):
    username: constr(min_length=1)
    password: constr(min_length=1)
    email: EmailStr
    mobile_nr: constr(min_length=1)


class LoginDto(BaseModel):
    username: str
    password: str


class userDto(BaseModel):
    username: str
    password: str
    email: str
    mobile_nr: str
    role: str
