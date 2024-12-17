from database import Database
from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Table, Boolean
from sqlalchemy.orm import relationship, sessionmaker


# todo:
# set role_id nullable=True to False
# set email unique=False to True


class User(Database.Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=False)
    mobile_nr = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)

    role = relationship("Role", back_populates="user")
    registration_codes = relationship("RegistrationCode", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(name={self.username}, email={self.email})>"


class Role(Database.Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False, unique=True)
    user = relationship("User", back_populates="role")

    def __init__(self, role):
        self.role = role


class RegistrationCode(Database.Base):
    __tablename__ = 'registration_code'
    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    type = Column(String, nullable=False)
    verified = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship("User", back_populates="registration_codes")

    def __init__(self, code, user):
        self.code = code.code
        self.type = code.type.value
        self.user = user
