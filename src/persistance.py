from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.declarative import declarative_base
from database import Database
import persistance_model
import model_dto


class Persistance():
    def __init__(self, config):
        self.db = Database(config)  # Use singleton
        self.session = self.db.get_session()

    def save_user(self, user: model_dto.userDto) -> None:
        #todo: user omvormen naar db_dto
        db_user: persistance_model.User = persistance_model.User()
        db_user.username = user.username
        db_user.password = user.password
        db_user.email = user.email
        db_user.mobile_nr = user.mobile_nr
        db_user.role = persistance_model.Role(user.role.value)

        self.session.add(db_user)
        self.session.commit()
        return True
    
    def save_role(self, role: model_dto.RoleEnum):
        db_role: persistance_model.Role = persistance_model.Role(role.value)
        self.session.add(db_role)
        self.session.commit()

    def get_user(self, username: str):
        db_user = self.session.query(persistance_model.User).filter_by(username=username).first()
        if db_user:
            user = model_dto.userDto(username = db_user.username,
                                    password = db_user.password,
                                    email = db_user.email,
                                    mobile_nr = db_user.mobile_nr,
                                    role = model_dto.RoleEnum(db_user.role.role))
            return user
        return None
    
    def get_users(self):
        db_users = self.session.query(persistance_model.User).all()
        users: List[model_dto.userDto]= []
        if db_users:
            for db_user in db_users:
                users.append(model_dto.userDto(username = db_user.username,
                                    password = db_user.password,
                                    email = db_user.email,
                                    mobile_nr = db_user.mobile_nr,
                                    role = model_dto.RoleEnum(db_user.role.role)))

        return users
    
    def add_or_update_registation_code(self, code: model_dto.RegistrationCodeDto):
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



# # Database setup
# engine = create_engine('sqlite:///database.db')  # Replace with your database URL
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)

# # Session setup
# Session = sessionmaker(bind=engine)
# session = Session()

# # Example usage
# if __name__ == "__main__":
#     # Create roles
#     admin_role = Role(role="Admin")
#     user_role = Role(role="User")
#     session.add_all([admin_role, user_role])
#     session.commit()



#     # Create users with roles
#     user1 = User(username="john_doe", password="securepassword", email="john@example.com", mobile_nr="1234567890", role=admin_role)
#     user2 = User(username="jane_doe", password="anotherpassword", email="jane@example.com", mobile_nr="0987654321", role=user_role)

#     existing_role = session.query(Role).filter_by(role="User").first()
#     user3 = User(username="jane_doe1", password="anotherpassword", email="jane1@example.com", mobile_nr="0987654321", role=existing_role)

#     session.add_all([user1, user2, user3])
#     session.commit()

#     # Query users and roles
#     users = session.query(User).all()
#     for user in users:
#         print(f"User: {user.username}, Role: {user.role.role}")