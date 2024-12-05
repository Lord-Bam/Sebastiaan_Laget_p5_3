import pytest
from persistance import Persistance
import model_dto
from model import Model
from model_dto import LoginDto
from mail import Mail
import configparser
from pydantic import ValidationError


@pytest.fixture()
def load_users():
    print("setup")
    p: Persistance = Persistance()
    p.users.append(
        model_dto.userDto(
            username="admin",
            password="admin_password",
            email="s.laget@scarlet.be",
            mobile_nr="123",
            role="admin",
        )
    )
    p.users.append(
        model_dto.userDto(
            username="user",
            password="user_password",
            email="s.laget@scarlet.be",
            mobile_nr="456",
            role="user",
        )
    )
    yield p
    print("teardown")
    # clean database


@pytest.fixture()
def create_model():
    print("setup")
    model = Model()
    yield model
    print("teardown")
    # clean database


@pytest.fixture()
def read_config():
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read("config.ini")
    return config


@pytest.fixture()
def setup_mail(read_config: configparser.ConfigParser):
    m: Mail = Mail(read_config)
    return m


@pytest.fixture()
def delete_mail(setup_mail: Mail):
    setup_mail.delete_all_mail()


class TestModel:

    @pytest.mark.parametrize(
        "username, password, expected",
        [
            ("admin", "admin_password", True),
            ("admin", "ff", False),
            ("admin", "", False),
            ("user", "user_password", True),
            ("user", "", False),
            ("", "", False),
        ],
    )
    def test_login(
        self, load_users: Persistance, username: str, password: str, expected: bool
    ):
        model: Model = Model()
        model.db = load_users
        login: LoginDto = LoginDto(username=username, password=password)
        result = model.login(login)
        assert result == expected

    @pytest.mark.parametrize(
        "username, password, email, mobile_nr, expected",
        [
            ("admin", "admin_password", "20240182b@gmail.com", "+32476880256", True),
        ],
    )
    def test_register_positive(
        self,
        delete_mail,
        setup_mail,
        create_model: Model,
        username: str,
        password: str,
        email: str,
        mobile_nr: str,
        expected: bool,
    ):
        user = model_dto.RegisterDto(
            username=username, password=password, email=email, mobile_nr=mobile_nr
        )
        model = create_model
        result = model.register(user)
        assert result == True
        result = model.get_user(username)
        assert result.username == username
        assert result.password == password
        assert result.email == email
        assert result.mobile_nr == mobile_nr
        mail: Mail = setup_mail
        message = mail.get_last_mail()
        assert message.body == "secret code = 666"
        assert message.subject == "registration mail"

    @pytest.mark.parametrize(
        "username, password, email, mobile_nr, field, exception",
        [
            (
                "",
                "admin_password",
                "20240182b@gmail.com",
                "+32476880256",
                "username",
                "String should have at least 1 character",
            ),
            (
                "admin",
                "",
                "20240182b@gmail.com",
                "+32476880256",
                "password",
                "String should have at least 1 character",
            ),
            (
                "admin",
                "admin_password",
                "",
                "+32476880256",
                "email",
                "value is not a valid email address: An email address must have an @-sign.",
            ),
            (
                "admin",
                "admin_password",
                "20240182b@gmail.com",
                "",
                "mobile_nr",
                "String should have at least 1 character",
            ),
            (
                "admin",
                "admin_password",
                "20240182b@",
                "+32476880256",
                "email",
                "value is not a valid email address: There must be something after the @-sign.",
            ),
        ],
    )
    def test_register_negative(
        self,
        create_model: Model,
        username: str,
        password: str,
        email: str,
        mobile_nr: str,
        field: str,
        exception: str,
    ):
        with pytest.raises(ValidationError) as exc_info:
            model_dto.RegisterDto(
                username=username, password=password, email=email, mobile_nr=mobile_nr
            )
        assert exc_info.value.errors()[0]["loc"] == (
            field,
        )  # Check which field caused the error
        assert exc_info.value.errors()[0]["msg"] == exception

    @pytest.mark.parametrize(
        "username, password, email, mobile_nr",
        [
            ("admin", "admin_password", "20240182b@gmail.com", "+32476880256"),
        ],
    )
    def test_verify_mail(
        self,
        delete_mail,
        setup_mail,
        create_model: Model,
        username: str,
        password: str,
        email: str,
        mobile_nr: str,
    ):
        user = model_dto.RegisterDto(
            username=username, password=password, email=email, mobile_nr=mobile_nr
        )
        model: Model = create_model
        model.register(user)
        mail: Mail = setup_mail
        message = mail.get_last_mail()
        assert message.body == "secret code = 666"
        assert message.subject == "registration mail"
        register_code: int = int(message.body.split(" ")[-1])
        assert model.verify_mail(register_code, username) == True
        assert model.verify_mail(1, username) == False
        # todo uncomment
        # assert model.verify_mail(register_code, "fdsa") == False
