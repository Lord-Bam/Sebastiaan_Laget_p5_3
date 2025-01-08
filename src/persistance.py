from typing import List, Optional
from database import Database
import persistance_model
import model_dto


class Persistance():
    def __init__(self, config):
        self.db = Database(config)  # Use singleton
        self.session = self.db.get_session()

    def add_update_user(self, user: model_dto.UserDto) -> None:
        db_user = self.session.query(persistance_model.User).filter_by(username=user.username).first()
        db_role = self.session.query(persistance_model.Role).filter_by(role=user.role).first()

        if not db_role:
            db_role = persistance_model.Role(user.role.value)

        if not db_user:
            db_user: persistance_model.User = persistance_model.User()
            db_user.username = user.username
            db_user.password = user.password
            db_user.email = user.email
            db_user.mobile_nr = user.mobile_nr
            db_user.role = db_role
            self.session.add(db_user)
        else:
            db_user.username = user.username
            db_user.password = user.password
            db_user.email = user.email
            db_user.mobile_nr = user.mobile_nr
            db_user.role = db_role
        self.session.commit()
        return True

    def add_update_role(self, role: model_dto.RoleEnum):
        db_role = self.session.query(persistance_model.Role).filter_by(role="role.value")
        if db_role:
            db_role.value = role.value
        else:
            self.session.add(db_role)
        self.session.commit()

    def get_user(self, username: str):
        db_user = self.session.query(persistance_model.User).filter_by(username=username).first()
        if db_user:
            user = model_dto.UserDto(username = db_user.username,
                                     password = db_user.password,
                                     email = db_user.email,
                                     mobile_nr = db_user.mobile_nr,
                                     role = model_dto.RoleEnum(db_user.role.role))
            return user
        return None

    def get_user_via_mail(self, mail: str):
        db_user = self.session.query(persistance_model.User).filter_by(email=mail).first()
        if db_user:
            user = model_dto.UserDto(username = db_user.username,
                                     password = db_user.password,
                                     email = db_user.email,
                                     mobile_nr = db_user.mobile_nr,
                                     role = model_dto.RoleEnum(db_user.role.role))
            return user
        return None
    
    def get_users(self):
        db_users = self.session.query(persistance_model.User).all()
        users: List[model_dto.UserDto]= []
        if db_users:
            for db_user in db_users:
                users.append(model_dto.UserDto(username = db_user.username,
                                               password = db_user.password,
                                               email = db_user.email,
                                               mobile_nr = db_user.mobile_nr,
                                               role = model_dto.RoleEnum(db_user.role.role)))

        return users
    
    def add_update_registation_code(self, code: model_dto.RegistrationCodeDto):
        db_user = self.session.query(persistance_model.User).filter_by(username=code.user.username).first()

        existing_code = self.session.query(persistance_model.RegistrationCode).filter_by(
            user_id = db_user.id,
            type = code.type
            ).first()

        if existing_code:
            #only updating verified since that's the only thing we need for now....
            #although for futureproofing I'm adding code as well :-)
            existing_code.code = code.code
            existing_code.verified = code.verified
        else:
            code = persistance_model.RegistrationCode(code, db_user)
            self.session.add(code)
        self.session.commit()


    def get_registation_code(self, username):
        db_user = self.session.query(persistance_model.User).filter_by(username=username).first()
        if db_user:
            db_registration_code: list["persistance_model.RegistrationCode"] = self.session.query(persistance_model.RegistrationCode).filter_by(user_id=db_user.id).all()
            registration_codes: list["model_dto.RegistrationCodeDto"] = []
            for db_registration_code in db_registration_code:
                registration_codes.append(model_dto.RegistrationCodeDto.model_validate(db_registration_code))
            return registration_codes
        else:
            return None