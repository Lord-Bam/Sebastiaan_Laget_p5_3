from persistance import Persistance
import model_dto


class TestPersistance:
    def test_get_user(self, setup_teardown, populate_database, get_config):
        config = get_config
        db_client = Persistance(config)
        # result_user = db_client.get_user("user")
        # result_admin = db_client.get_user("admin")
        # result_user == populate_database[0]
        # result_admin == populate_database[1]
        assert len(db_client.get_users()) == 2
        assert db_client.get_user("fdas") is None

    def test_save_user(self, setup_teardown, get_config):
        p = Persistance(get_config)
        role = model_dto.RoleEnum("admin")
        user = model_dto.UserDto(
            username="admin",
            password="password",
            email="20240182b@gmail.com",
            mobile_nr="123",
            role=role
        )
        p.add_update_user(user)
        result = p.get_user("admin")
        assert result.username == user.username
        assert result.password == user.password
        assert result.email == user.email
        assert result.mobile_nr == user.mobile_nr
        assert result.role.value == "admin"

    def test_save_roles(serlf, setup_teardown, get_config):
        p = Persistance(get_config)
        admin_role = model_dto.RoleEnum("admin")
        user_role = model_dto.RoleEnum("user")
        p.add_update_role(admin_role)
        p.add_update_role(user_role)

    def test_save_registration_codes(self, setup_teardown, populate_database, get_config):
        p = Persistance(get_config)
        result_user = populate_database[0]
        result_admin = populate_database[1]
        admin: model_dto.UserDto = model_dto.UserDto.model_validate(result_user)
        usercode_sms = model_dto.RegistrationCodeDto(code="1230", type="sms", user=admin, verified=False)
        usercode_mail = model_dto.RegistrationCodeDto(code="1230", type="mail", user=result_admin, verified=False)
        p.add_update_registation_code(usercode_sms)
        p.add_update_registation_code(usercode_mail)

    def test_get_registration_codes(self, setup_teardown, populate_database, get_config):
        p = Persistance(get_config)
        result_admin = populate_database[1]
        admin: model_dto.UserDto = model_dto.UserDto.model_validate(result_admin)
        usercode_sms = model_dto.RegistrationCodeDto(code="1234", type="sms", user=result_admin, verified=False)
        usercode_mail = model_dto.RegistrationCodeDto(code="5678", type="mail", user=result_admin, verified=False)
        p.add_update_registation_code(usercode_sms)
        p.add_update_registation_code(usercode_mail)
        result = p.get_registation_code("admin")
        assert result[0].user.username == "admin"
        assert result[1].user.username == "admin"
        assert result[0].code == "1234"
        assert result[1].code == "5678"
        assert result[0].type == "sms"
        assert result[1].type == "mail"
        assert result[0].verified == False
        assert result[1].verified == False