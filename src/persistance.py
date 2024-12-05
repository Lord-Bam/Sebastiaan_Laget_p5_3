from pydantic import BaseModel
from model_dto import userDto
from typing import List, Optional


class Persistance():
    def __init__(self, config):
        self.users: List[userDto] = []

    def save_user(self, user: userDto) -> None:
        self.users.append(user)
        return True

    def get_user(self, username: str) -> Optional[userDto]:
        for user in self.users:
            if user.username == username:
                return user
    
    def get_users(self,) -> List[userDto]:
        return self.users
