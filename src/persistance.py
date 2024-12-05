from pydantic import BaseModel
from model_dto import userDto
from typing import List
from model_dto import RegisterDto


class Persistance(BaseModel):
    users: List[userDto] = []

    def save_user(self, user: userDto) -> None:
        self.users.append(user)
        pass

    def get_user(self, username: str) -> userDto:
        for user in self.users:
            if user.username == username:
                return user
        return userDto(username="", password="", email="", mobile_nr="", role="")

    def resister_user(self, register_user: RegisterDto) -> bool:
        user: userDto = userDto(
            username=register_user.username,
            password=register_user.password,
            email=register_user.email,
            mobile_nr=register_user.mobile_nr,
            role="user",
        )
        self.users.append(user)
        return True
