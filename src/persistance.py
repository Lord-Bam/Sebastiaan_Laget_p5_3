from pydantic import BaseModel
from model_dto import userDto
from typing import List, Optional
from model_dto import RegistrationCodeDto
from model_dto import CodeTypeEnum


class Persistance():
    def __init__(self, config):
        self.users: List[userDto] = []
        self.codes: List[RegistrationCodeDto] = []

    def save_user(self, user: userDto) -> None:
        self.users.append(user)
        return True

    def get_user(self, username: str) -> Optional[userDto]:
        for user in self.users:
            if user.username == username:
                return user
    
    def get_users(self,) -> List[userDto]:
        return self.users
    
    def save_registation_code(self, code: RegistrationCodeDto):
        self.codes.append(code)

    def get_registation_code(self, username: str, type: CodeTypeEnum) -> int:
        for code in self.codes:
            if code.username == username and code.type == type:
                return code
        return 0