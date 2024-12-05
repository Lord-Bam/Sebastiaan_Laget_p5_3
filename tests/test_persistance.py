import pytest
from persistance import Persistance
from model_dto import userDto


@pytest.fixture()
def connect_to_db():
    print("setup")
    db = Persistance()
    yield db
    print("teardown")


@pytest.fixture()
def save_users():
    print("setup")
    db = Persistance()
    db.save_user(  # type: ignore
        userDto(
            username="user",
            password="password",
            email="s.laget@scarlet.be",
            mobile_nr="456",
            role="user",
        )
    )
    db.save_user(  # type: ignore
        userDto(
            username="admin",
            password="password",
            email="s.laget@scarlet.be",
            mobile_nr="123",
            role="admin",
        )
    )
    yield db
    print("teardown")


class TestPersistance:
    def test_save_user(self, connect_to_db: Persistance):
        db = connect_to_db
        db.save_user(
            userDto(
                username="user",
                password="password",
                email="s.laget@scarlet.be",
                mobile_nr="456",
                role="user",
            )
        )
        db.save_user(
            userDto(
                username="admin",
                password="password",
                email="s.laget@scarlet.be",
                mobile_nr="123",
                role="admin",
            )
        )
        assert db.get_user("user").username == "user"
        assert db.get_user("admin").username == "admin"

    def test_get_user(self, save_users: Persistance):
        db = save_users
        assert db.get_user("user").username == "user"
        assert db.get_user("admin").username == "admin"
        assert len(db.users) == 2
        assert db.get_user("fdas").username == ""
