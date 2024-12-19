import pytest
import configparser
from persistance_model import User
from persistance_model import Role
from database import Database
from werkzeug.security import generate_password_hash
from model import Model
from model_dto import UserDto


#todo: add roles
#todo: uncomment roles when populating database



@pytest.fixture()
def get_config():
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read("config.ini")
    return config


@pytest.fixture()
def db_singleton(get_config):
    db = Database(get_config)  # Ensure singleton is initialized
    yield db


@pytest.fixture()
def get_db_session(db_singleton):
    session = db_singleton.get_session()
    yield session
    session.close()


@pytest.fixture()
def clean_database(db_singleton):
    print("setup: deleting database")
    db_singleton.drop_all()
    db_singleton.create_all()
    yield
    print("Teardown: deleting database")
    db_singleton.drop_all()



@pytest.fixture()
def populate_database(get_db_session):
    session = get_db_session
    admin_role = Role(role="admin")
    user_role = Role(role="user")
    admin = User(
            username="admin",
            password=generate_password_hash("admin_password"),
            email="20240182b@gmail.com",
            mobile_nr="123",
            role=admin_role,
        )

    user = User(
            username="user",
            password=generate_password_hash("user_password"),
            email="20240182b@gmail.com",
            mobile_nr="456",
            role=user_role,
        )
    session.add(admin)
    session.add(user)
    session.commit()
    return user, admin

@pytest.fixture()
def setup_teardown(clean_database):
    print("setup")
    yield
    print("Teardown")


@pytest.fixture()
def setup_x():
    print("setup x")
    yield
    print("setup y")

@pytest.fixture()
def create_users(get_config):
    users = [
            UserDto(username="admin", password="admin_password", email="20240182b@gmail.com", mobile_nr="+32476880256"),
            UserDto(username="user", password="user_password", email="20240182b@gmail.com", mobile_nr="+32476880256"),
        ]
    model: Model = Model(get_config)
    for user in users:
        model.register(user)

    return users