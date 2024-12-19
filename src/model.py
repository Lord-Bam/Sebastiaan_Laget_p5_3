import model_dto
from persistance import Persistance
from model_dto import LoginDto
from model_dto import UserDto
import configparser
from tools import Mail
from tools import SMSService
import random
from model_dto import RegistrationCodeDto
from model_dto import RoleEnum
from model_dto import CodeTypeEnum
from werkzeug.security import generate_password_hash, check_password_hash


class Model:
    db: Persistance
    mail: Mail

    def __init__(self, config = configparser.ConfigParser()):
        self.db: Persistance = Persistance(config)
        self.mail: Mail = Mail(config)
        self.sms_client: SMSService = SMSService(config)

    def login(self, login_dto: LoginDto) -> str:
        #todo
        #verify if registration codes are verified.
        user_dto = self.get_user(login_dto.username)

        if not user_dto:
            return "user_not_found"

        sms_code: model_dto.RegistrationCodeDto = self.get_registration_sms_code_from_user(user_dto)
        if sms_code:
            if not sms_code.verified:
                return "verify_sms"

        mail_code: model_dto.RegistrationCodeDto = self.get_registration_mail_code_from_user(user_dto)
        if mail_code:
            if not mail_code.verified:
                return "verify_mail"

        if check_password_hash(user_dto.password, login_dto.password):
            return "True"

        return "Username of password incorrect."

    def verify_registration_code(self, code: model_dto.RegistrationCodeDto):
        registration_codes: list[model_dto.RegistrationCodeDto] = self.db.get_registation_code(code.user.username)
        for code_under_test in registration_codes:
            if code_under_test.type == code.type:
                if code_under_test.code == code.code:
                    code_under_test.verified = True
                    self.db.add_update_registation_code(code_under_test)
                    return True
        return False

    def get_registration_codes_from_user(self, user: model_dto.UserDto):
        registration_codes: list["model_dto.RegistrationCodeDto"] = self.db.get_registation_code(user.username)
        return registration_codes


    def get_registration_mail_code_from_user(self, user: model_dto.UserDto):
        registration_codes: list["model_dto.RegistrationCodeDto"] = self.db.get_registation_code(user.username)
        if registration_codes:
            for code in registration_codes:
                if code.type == "mail":
                    return code
        return None

    def get_registration_sms_code_from_user(self, user: model_dto.UserDto):
        registration_codes: list["model_dto.RegistrationCodeDto"] = self.db.get_registation_code(user.username)
        if registration_codes:
            for code in registration_codes:
                if code.type == "sms":
                    return code
        return None



    def register(self, user: model_dto.UserDto) -> bool:
        try:
            # save user
            user.password = generate_password_hash(user.password)
            if len(self.get_users()) == 0:
                user.role=RoleEnum("admin")
            else:
                user.role=RoleEnum("user")
            self.db.add_update_user(user)
            
            # send mail
            code = str(random.randint(1000, 9999))
            self.db.add_update_registation_code(RegistrationCodeDto(code=code, type="mail", user=user, verified=False))
            #self.send_register_mail(user, code)
            
            
            # send sms
            code = str(random.randint(1000, 9999))
            self.db.add_update_registation_code(RegistrationCodeDto(code=code, type="sms", user=user, verified=False))
            #self.send_register_sms(user.mobile_nr, f"this is your personal registration code: {code}")
            return True
        except Exception as ex:
            print(ex)
            return False

    def send_register_mail(self, user: model_dto.UserDto, code):
        body: str = f"secret code = {code}"
        subject: str = "registration mail"
        email: str = user.email
        result = self.mail.send_email(subject, body, email)
        print(result)

    def send_register_sms(self, mobile_nr: str, body: str):
        self.sms_client.send_sms(mobile_nr, body)
        pass

    def get_user(self, username: str):
        return self.db.get_user(username)
    
    def get_users(self) -> list[model_dto.UserDto]:
        return self.db.get_users()

#     def verify_mail(self, register_code: int, username: str):
#         # get user verification code from database
#         if register_code == 666:
#             return True
#         else:
#             return False
#         pass

#     def verify_mobile_nr(self):
#         pass

#     def logout(self):
#         pass

#     def reset_password(self):
#         pass

# class userDto(BaseModel):
#     username: constr(min_length=1)
#     password: constr(min_length=1)
#     email: EmailStr
#     mobile_nr: str
#     role: str

# class CodeTypeEnum(str, Enum):
#     mail = "mail"
#     sms = "sms"

# class RegistrationCodeDto(BaseModel):
#     username: constr(min_length=1)
#     code: conint(ge=1000, le=9999)
#     type: CodeTypeEnum