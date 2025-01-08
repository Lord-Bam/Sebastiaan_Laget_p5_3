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
from jinja2 import Environment, FileSystemLoader
import jwt
import datetime



class Model:
    db: Persistance
    mail: Mail

    def __init__(self, config = configparser.ConfigParser()):
        self.db: Persistance = Persistance(config)
        self.mail: Mail = Mail(config)
        self.sms_client: SMSService = SMSService(config)
        # Set up Jinja2 environment
        env = Environment(loader=FileSystemLoader(config['MAIL TEMPLATES']['directory']))
        # Load the template
        self.reset_template = env.get_template(config['MAIL TEMPLATES']['reset_mail'])
        self.webserver_address = config['WEBSERVER']['address']
        self.jwt_key = config['JWT']['key']

    def login(self, login_dto: LoginDto) -> str:
        #todo
        #verify if registration codes are verified.
        user_dto = self.get_user(login_dto.username)

        if not user_dto:
            return "user_not_found"

        if check_password_hash(user_dto.password, login_dto.password):
            sms_code: model_dto.RegistrationCodeDto = self.get_registration_sms_code_from_user(user_dto)
            if sms_code:
                if not sms_code.verified:
                    return "verify_sms"

            mail_code: model_dto.RegistrationCodeDto = self.get_registration_mail_code_from_user(user_dto)
            if mail_code:
                if not mail_code.verified:
                    return "verify_mail"
            return "True"
        return "Username or password incorrect."

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

    def update_user(self, user: model_dto.UserDto) -> bool:
        try:
            user.password = generate_password_hash(user.password)
            self.db.add_update_user(user)
        except Exception as ex:
            print(ex)
            return False

    def send_reset_mail(self, mail: str):
        #check if user exists
        user = self.db.get_user_via_mail(mail)
        #send mail, include jwt token so we can afterwards verify if the link is real.
        if user:
            #generate reset link:
            expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=100)
            payload={
                "padding":"padding",
                "email":mail
            }
            jwt_token = jwt.encode(payload, "secret_key", algorithm='HS256')
            print(jwt_token)
            reset_link = self.webserver_address + "/reset_password?token=" + jwt_token

            #using jinja2, create the html mail and send it.
            body = self.reset_template.render(reset_link=reset_link)
            print(body)
            subject: str = "reset mail"
            email: str = mail
            result = self.mail.send_email(subject, body, email, "html")
            print(result)
        pass