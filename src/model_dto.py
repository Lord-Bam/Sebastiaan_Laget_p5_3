from pydantic import BaseModel, EmailStr, constr, conint
from enum import Enum

class LoginDto(BaseModel):
    username: str
    password: str


class userDto(BaseModel):
    username: constr(min_length=1)
    password: constr(min_length=1)
    email: EmailStr
    mobile_nr: str
    role: str

class CodeTypeEnum(str, Enum):
    mail = "mail"
    sms = "sms"

class RegistrationCodeDto(BaseModel):
    username: constr(min_length=1)
    code: conint(ge=1000, le=9999)
    type: CodeTypeEnum
