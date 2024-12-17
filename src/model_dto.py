from pydantic import BaseModel, EmailStr, constr, conint, ConfigDict, field_validator, Field
from enum import Enum
from typing import Optional
import persistance_model

class LoginDto(BaseModel):
    username: str
    password: str

class RoleEnum(str, Enum):

    model_config = ConfigDict(from_attributes=True)

    admin = "admin"
    user = "user"

class userDto(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    username: constr(min_length=1)
    password: constr(min_length=1)
    email: EmailStr
    mobile_nr: str
    role: Optional[RoleEnum]= None

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, value):
        if isinstance(value, persistance_model.Role):
            return value.role
        return value

class CodeTypeEnum(str, Enum):
    mail = "mail"
    sms = "sms"

class RegistrationCodeDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: constr(min_length=4, max_length=4)
    type: CodeTypeEnum
    verified: bool = Field(default=False)
    user: userDto