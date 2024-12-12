import model_dto
from persistance import Persistance
from model_dto import LoginDto
from model_dto import userDto
import configparser
from mail import Mail
from sms import SMSService
import random
from model_dto import RegistrationCodeDto


class Model:
    db: Persistance
    mail: Mail

    def __init__(self, config = configparser.ConfigParser()):
        self.db: Persistance = Persistance(config)
        self.mail: Mail = Mail(config)
        self.sms_client: SMSService = SMSService(config)

    def login(self, login_dto: LoginDto) -> bool:
        # get user.
        user: userDto = self.db.get_user(username=login_dto.username)
        print(user)
        if login_dto.username != "":
            if login_dto.password == user.password:
                return True
        # else:
        #     return False
        return False

    def register(self, user: model_dto.userDto) -> bool:
        try:
            # save user
            if len(self.get_users()) == 0:
                user.role="admin"
            else:
                user.role="user"
            self.db.save_user(user)
            
            # send mail
            code = random.randint(1000, 9999)
            self.db.save_registation_code(RegistrationCodeDto(username=user.username, code=code, type="mail"))
            self.send_register_mail(user, code)
            
            
            # send sms
            code = random.randint(1000, 9999)
            self.db.save_registation_code(RegistrationCodeDto(username=user.username, code=code, type="sms"))
            self.send_register_sms(user.mobile_nr, f"this is your personal registration code: {code}")
            return True
        
        
        except Exception as ex:
            print(ex)
            return False

    def send_register_mail(self, user: model_dto.userDto, code):
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
    
    def get_users(self):
        return self.db.get_users()

    def verify_mail(self, register_code: int, username: str):
        # get user verification code from database
        if register_code == 666:
            return True
        else:
            return False
        pass

    def verify_mobile_nr(self):
        pass

    def logout(self):
        pass

    def reset_password(self):
        pass
