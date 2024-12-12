import pytest
from persistance import Persistance
from model import Model
from model_dto import LoginDto
from mail import Mail
import configparser
from pydantic import ValidationError
from test_data import login_data, users, users_list
from model_dto import userDto
from model_dto import RegistrationCodeDto


class TestModel:
    @pytest.mark.parametrize("username, password, expected",login_data)
    def test_login(
        self, db_client, get_model, username: str, password: str, expected: bool
    ):
        model: Model = get_model

        #######################################
        #bit ugly here, but since the user array has to be in model this is the cleanest way.... :-(
        #######################################
        user = db_client.save_user(  # type: ignore
            userDto(
                username="user",
                password="user_password",
                email="20240182b@gmail.com",
                mobile_nr="456",
                role="user",
            )
        )
        admin = db_client.save_user(  # type: ignore
            userDto(
                username="admin",
                password="admin_password",
                email="20240182b@gmail.com",
                mobile_nr="123",
                role="admin",
            )
        )
        model.db = db_client
        ##############################################################

        login: LoginDto = LoginDto(username=username, password=password)
        result = model.login(login)
        assert result == expected


    @pytest.mark.parametrize("users_list", users_list)
    def test_user_registration_roles(self,get_model: Model, users_list):
        model = get_model
        for user in users_list:
            result = model.register(user)
            assert result == True

        result: list[userDto]= model.get_users()
        for user in result:
            if user.username == "admin":
                assert user.role == "admin"
            else:
                assert user.role == "user"

    @pytest.mark.parametrize("user", users)
    def test_register_positive(
        self,
        mail_client: Mail,
        get_model: Model,
        user
    ):
        model = get_model
        result = model.register(user)
        assert result == True
        result = model.get_user(user.username)
        assert result.username == user.username
        assert result.password == user.password
        assert result.email == user.email
        assert result.mobile_nr == user.mobile_nr

        #verify mail:
        code: RegistrationCodeDto = model.db.get_registation_code(user.username, "mail")
        message = mail_client.get_last_mail()
        assert message.body == f"secret code = {code.code}"
        assert message.subject == "registration mail"


    # @pytest.mark.parametrize(
    #     "username, password, email, mobile_nr, field, exception",
    #     [
    #         (
    #             "",
    #             "admin_password",
    #             "20240182b@gmail.com",
    #             "+32476880256",
    #             "username",
    #             "String should have at least 1 character",
    #         ),
    #         (
    #             "admin",
    #             "",
    #             "20240182b@gmail.com",
    #             "+32476880256",
    #             "password",
    #             "String should have at least 1 character",
    #         ),
    #         (
    #             "admin",
    #             "admin_password",
    #             "",
    #             "+32476880256",
    #             "email",
    #             "value is not a valid email address: An email address must have an @-sign.",
    #         ),
    #         (
    #             "admin",
    #             "admin_password",
    #             "20240182b@gmail.com",
    #             "",
    #             "mobile_nr",
    #             "String should have at least 1 character",
    #         ),
    #         (
    #             "admin",
    #             "admin_password",
    #             "20240182b@",
    #             "+32476880256",
    #             "email",
    #             "value is not a valid email address: There must be something after the @-sign.",
    #         ),
    #     ],
    # )
    # def test_register_negative(
    #     self,
    #     create_model: Model,
    #     username: str,
    #     password: str,
    #     email: str,
    #     mobile_nr: str,
    #     field: str,
    #     exception: str,
    # ):
    #     with pytest.raises(ValidationError) as exc_info:
    #         model_dto.RegisterDto(
    #             username=username, password=password, email=email, mobile_nr=mobile_nr
    #         )
    #     assert exc_info.value.errors()[0]["loc"] == (
    #         field,
    #     )  # Check which field caused the error
    #     assert exc_info.value.errors()[0]["msg"] == exception

    # @pytest.mark.parametrize(
    #     "username, password, email, mobile_nr",
    #     [
    #         ("admin", "admin_password", "20240182b@gmail.com", "+32476880256"),
    #     ],
    # )
    # def test_verify_mail(
    #     self,
    #     delete_mail,
    #     setup_mail,
    #     create_model: Model,
    #     username: str,
    #     password: str,
    #     email: str,
    #     mobile_nr: str,
    # ):
    #     user = model_dto.RegisterDto(
    #         username=username, password=password, email=email, mobile_nr=mobile_nr
    #     )
    #     model: Model = create_model
    #     model.register(user)
    #     mail: Mail = setup_mail
    #     message = mail.get_last_mail()
    #     assert message.body == "secret code = 666"
    #     assert message.subject == "registration mail"
    #     register_code: int = int(message.body.split(" ")[-1])
    #     assert model.verify_mail(register_code, username) == True
    #     assert model.verify_mail(1, username) == False
    #     # todo uncomment
    #     # assert model.verify_mail(register_code, "fdsa") == False
