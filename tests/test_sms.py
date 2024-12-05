import pytest
import configparser
from sms import SMSService


@pytest.fixture()
def read_config():
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read("config.ini")
    return config


@pytest.fixture()
def sms_client(read_config: configparser.ConfigParser):
    config = read_config
    config.read("config.ini")
    sms_client = SMSService(config)
    return sms_client


def test_sms(read_config: configparser.ConfigParser, sms_client: SMSService):
    sms_client.send_sms("+32476880256", "dit is een test")
    assert True
