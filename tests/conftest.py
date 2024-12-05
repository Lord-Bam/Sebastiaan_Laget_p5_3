import pytest
import configparser
from sms import SMSService
from mail import Mail
from persistance import Persistance
from model_dto import userDto
from model import Model

@pytest.fixture()
def config():
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read("config.ini")
    return config


@pytest.fixture()
def sms_client(config: configparser.ConfigParser):
    sms_client = SMSService(config)
    return sms_client

@pytest.fixture()
def mail_client(config: configparser.ConfigParser):
    m: Mail = Mail(config)
    return m


@pytest.fixture()
def db_client(config: configparser.ConfigParser):
    p: Persistance = Persistance(config)
    return p

@pytest.fixture()
def populate_database(db_client: Persistance):
    user = db_client.save_user(  # type: ignore
        userDto(
            username="user",
            password="password",
            email="20240182b@gmail.com",
            mobile_nr="456",
            role="user",
        )
    )
    admin = db_client.save_user(  # type: ignore
        userDto(
            username="admin",
            password="password",
            email="20240182b@gmail.com",
            mobile_nr="123",
            role="admin",
        )
    )
    return user, admin

@pytest.fixture()
def get_model(config):
    model = Model(config)
    return model