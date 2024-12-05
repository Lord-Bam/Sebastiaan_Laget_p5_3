import pytest
from persistance import Persistance
from model_dto import userDto


class TestPersistance:
    def test_get_user(self, populate_database ,db_client: Persistance):
        result_user = db_client.get_user("user")
        result_admin = db_client.get_user("admin")

        result_user == populate_database[0]
        result_admin == populate_database[1]
        assert len(db_client.users) == 2
        assert db_client.get_user("fdas") ==  None

    def test_save_user(self, db_client: Persistance):
        db_client.save_user(
            userDto(
                username="user",
                password="password",
                email="s.laget@scarlet.be",
                mobile_nr="456",
                role="user",
            )
        )
        db_client.save_user(
            userDto(
                username="admin",
                password="password",
                email="s.laget@scarlet.be",
                mobile_nr="123",
                role="admin",
            )
        )
        assert db_client.get_user("user").username == "user"
        assert db_client.get_user("admin").username == "admin"