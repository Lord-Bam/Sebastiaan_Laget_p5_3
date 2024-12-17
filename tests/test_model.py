import pytest

import model_dto
from persistance import Persistance
from model import Model
from mail import Mail
from pydantic import ValidationError
from model_dto import LoginDto
from test_data import login_data, register_list
from model_dto import userDto



class TestModel:
    @pytest.mark.parametrize("username, password, expected", login_data)
    def test_login(
        self, setup_teardown, get_config, populate_database,  username: str, password: str, expected: bool
    ):
        model: Model = Model(get_config)
        login: LoginDto = LoginDto(username=username, password=password)
        result = model.login(login)
        assert result == expected


    @pytest.mark.parametrize("register_list", register_list)
    def test_user_registration_roles(self,setup_teardown, get_config, register_list):
        model: Model = Model(get_config)
        for user in register_list:
            result = model.register(user)
            assert result == True

        users: list[model_dto.userDto]= model.get_users()

        for user in users:
            assert type(user) == model_dto.userDto
            if user.username == "admin":
                assert user.role == "admin"
            if user.username == "user":
                assert user.role == "user"


    @pytest.mark.parametrize("register_list", register_list)
    def test_registration_code(self,setup_teardown, get_config, register_list):
        #register 2 users
        model: Model = Model(get_config)
        for user in register_list:
            result = model.register(user)
            assert result == True

        #Verify user codes
        admin_codes: list["model_dto.RegistrationCodeDto"] = model.get_registration_codes_from_user(register_list[0])
        assert len(admin_codes) == 2
        assert admin_codes[0].type == "sms" or admin_codes[1].type == "sms"
        assert admin_codes[0].type == "mail" or admin_codes[1].type == "mail"
        assert admin_codes[0].verified == False
        assert admin_codes[1].verified == False
        assert admin_codes[0].user.username == "admin"
        assert admin_codes[1].user.username == "admin"

        user_codes: list["model_dto.RegistrationCodeDto"] = model.get_registration_codes_from_user(register_list[1])
        assert len(admin_codes) == 2
        assert user_codes[0].type == "sms" or user_codes[1].type == "sms"
        assert user_codes[0].type == "mail" or user_codes[1].type == "mail"
        assert user_codes[0].verified == False
        assert user_codes[1].verified == False
        assert user_codes[0].user.username == "user"
        assert user_codes[1].user.username == "user"


        #verify verification function
        #Since we don't know the codes, we first need to get them.
        admin_dto: model_dto.userDto = register_list[0]
        admin_mail_code: model_dto.RegistrationCodeDto = model.get_registration_mail_codes_from_user(admin_dto)
        admin_sms_code: model_dto.RegistrationCodeDto  = model.get_registration_sms_codes_from_user(admin_dto)

        #since these are just registerd, codes should be false
        assert admin_mail_code.verified == False
        assert admin_sms_code.verified == False


        #verify the code
        model.verify_registration_code(admin_mail_code)
        model.verify_registration_code(admin_sms_code)

        #fetch codes and check if they are verified
        admin_mail_code: model_dto.RegistrationCodeDto = model.get_registration_mail_codes_from_user(admin_dto)
        admin_sms_code: model_dto.RegistrationCodeDto  = model.get_registration_sms_codes_from_user(admin_dto)
        assert admin_mail_code.verified == True
        assert admin_sms_code.verified == True



    # @pytest.mark.parametrize("user", users)
    # def test_register_positive(
    #     self,
    #     mail_client: Mail,
    #     get_model: Model,
    #     user
    # ):
    #     model = get_model
    #     result = model.register(user)
    #     assert result == True
    #     result = model.get_user(user.username)
    #     assert result.username == user.username
    #     assert result.password == user.password
    #     assert result.email == user.email
    #     assert result.mobile_nr == user.mobile_nr

    #     #verify mail:
    #     code: RegistrationCodeDto = model.db.get_registation_code(user.username, "mail")
    #     message = mail_client.get_last_mail()
    #     assert message.body == f"secret code = {code.code}"
    #     assert message.subject == "registration mail"


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
