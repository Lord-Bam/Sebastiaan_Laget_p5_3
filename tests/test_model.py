import pytest
import model_dto
from model_dto import LoginDto, RegistrationCodeDto, CodeTypeEnum
from test_data import login_data
from model import Model


class TestModel:
    @pytest.mark.parametrize("username, password, expected", login_data )
    def test_login(
        self, setup_teardown, get_config, username: str, password: str, expected: bool, create_users
    ):
        model: Model = Model(get_config)
        admin = create_users[0]

        #Since admin codes are random generated, get the admin code.
        admin_mail_code: "model_dto.RegistrationCodeDto" = model.get_registration_mail_code_from_user(create_users[0])
        admin_sms_code: "model_dto.RegistrationCodeDto" = model.get_registration_sms_code_from_user(create_users[0])

        #verify sms:
        login_dto = LoginDto(username=admin.username, password=admin.password)
        assert model.login(login_dto) == "verify_sms"
        verification_dto = RegistrationCodeDto(code=admin_sms_code.code, verified=True, type=CodeTypeEnum("sms"), user=admin)
        model.verify_registration_code(verification_dto)

        #verify mail
        assert model.login(login_dto) == "verify_mail"
        verification_dto = RegistrationCodeDto(code=admin_mail_code.code, verified=True, type=CodeTypeEnum("mail"), user=admin)
        model.verify_registration_code(verification_dto)

        login: LoginDto = LoginDto(username=username, password=password)
        result = model.login(login)
        assert result == expected

    def test_reset_password(self, setup_teardown, get_config, create_users):
        model: Model = Model(get_config)
        admin = create_users[0]
        login_dto = LoginDto(username="admin", password="admin_password")
        assert model.login(login_dto) == "verify_sms"
        admin.password = "123"
        admin.mobile_nr = "123"
        model.update_user(admin)
        login_dto = LoginDto(username="admin", password="123")
        assert model.login(login_dto) == "verify_sms"
        login_dto = LoginDto(username="admin", password="123")
        assert model.login(login_dto) != "admin_password"



    def test_user_registration_roles(self,setup_teardown, get_config, create_users):
        model: Model = Model(get_config)
        users: list[model_dto.UserDto]= model.get_users()

        for user in users:
            assert type(user) == model_dto.UserDto
            if user.username == "admin":
                assert user.role == "admin"
            if user.username == "user":
                assert user.role == "user"


    def test_registration_code(self,setup_teardown, create_users, get_config):
        #register 2 users
        model: Model = Model(get_config)

        #Verify user codes
        admin_codes: list["model_dto.RegistrationCodeDto"] = model.get_registration_codes_from_user(create_users[0])
        assert len(admin_codes) == 2
        assert admin_codes[0].type == "sms" or admin_codes[1].type == "sms"
        assert admin_codes[0].type == "mail" or admin_codes[1].type == "mail"
        assert admin_codes[0].verified == False
        assert admin_codes[1].verified == False
        assert admin_codes[0].user.username == "admin"
        assert admin_codes[1].user.username == "admin"

        user_codes: list["model_dto.RegistrationCodeDto"] = model.get_registration_codes_from_user(create_users[1])
        assert len(admin_codes) == 2
        assert user_codes[0].type == "sms" or user_codes[1].type == "sms"
        assert user_codes[0].type == "mail" or user_codes[1].type == "mail"
        assert user_codes[0].verified == False
        assert user_codes[1].verified == False
        assert user_codes[0].user.username == "user"
        assert user_codes[1].user.username == "user"


        #verify verification function
        #Since we don't know the codes, we first need to get them.
        admin_dto: model_dto.UserDto = create_users[0]
        admin_mail_code: model_dto.RegistrationCodeDto = model.get_registration_mail_code_from_user(admin_dto)
        admin_sms_code: model_dto.RegistrationCodeDto  = model.get_registration_sms_code_from_user(admin_dto)

        #since these are just registerd, codes should be false
        assert admin_mail_code.verified == False
        assert admin_sms_code.verified == False


        #verify the code
        model.verify_registration_code(admin_mail_code)
        model.verify_registration_code(admin_sms_code)

        #fetch codes and check if they are verified
        admin_mail_code: model_dto.RegistrationCodeDto = model.get_registration_mail_code_from_user(admin_dto)
        admin_sms_code: model_dto.RegistrationCodeDto  = model.get_registration_sms_code_from_user(admin_dto)
        assert admin_mail_code.verified == True
        assert admin_sms_code.verified == True