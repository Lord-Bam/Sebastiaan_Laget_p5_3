from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Table
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association table to represent many-to-many relationship
user_roles = Table('user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # Relationship to User
    users = relationship("User", secondary=user_roles, back_populates="roles")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    name = Column(String)
    age = Column(Integer)
    roles = [Role]
    # Relationship to Role (many-to-many relationship)
    roles = relationship("Role", secondary=user_roles, back_populates="users")


# Assuming session is already created with your engine

# Example: Add some roles and users

engine = create_engine('sqlite:///example.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


admin_role = Role(name='Admin')
user_role = Role(name='User')
session.add(admin_role)
session.add(user_role)

user1 = User(username='johndoe', name='John Doe', age=30, roles=[admin_role, user_role])
user2 = User(username='janedoe', name='Jane Doe', age=28, roles=[user_role])
session.add(user1)
session.add(user2)

session.commit()

users_with_role = session.query(User).join(user_roles).join(Role).filter(Role.name == "Admin").all()

for user in users_with_role:
    print(f"User: {user.username}, Roles: {[role.name for role in user.roles]}")