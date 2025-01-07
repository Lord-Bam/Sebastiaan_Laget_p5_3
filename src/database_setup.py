from model_dto import UserDto
from model import Model
import configparser
from database import Database


def create_users():
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read("config.ini")
    db = Database(config)  # Ensure singleton is initialized
    session = db.get_session()
    db.drop_all()
    db.create_all()
    users = [
            UserDto(username="admin", password="admin_password", email="20240182b@gmail.com", mobile_nr="+32476880256"),
            UserDto(username="user", password="user_password", email="20240182b@gmail.com", mobile_nr="+32476880256"),
        ]

    model: Model = Model(config)
    for user in users:
        model.register(user)

    for code in model.get_registration_codes_from_user(users[0]):
        print(code.user.username, code.type, code.code)
    for code in model.get_registration_codes_from_user(users[1]):
        print(code.user.username, code.type, code.code)

def setup_database():
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read("config.ini")
    db = Database(config)  # Ensure singleton is initialized
    session = db.get_session()
    print("setup: deleting database")
    db.drop_all()
    db.create_all()
    session.close()


setup_database()
create_users()
