from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class for the ORM
Base = declarative_base()

# Define a model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer)

# Create a database engine (replace `sqlite:///example.db` with your database URL)
engine = create_engine('sqlite:///example.db')

# Create tables in the database
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()

# Create an instance of the User model
new_user = User(name="John Doe", age=30)
new_user1 = User(name="bas", age=30)
# Add the new user to the session
session.add(new_user)
session.add(new_user1)

# Commit the session to save the user to the database
session.commit()

# Verify the saved user
print(f"User saved with ID: {new_user.id}")


user_id = 1  # Example user ID
retrieved_user = session.query(User).filter_by(id=1).first()

if retrieved_user:
    print(f"User Found: {retrieved_user.name}, Age: {retrieved_user.age}")
else:
    print("User not found")

users = session.query(User).all()
for user in users:
    print(f"User: {user.name}, Age: {user.age}")


users = session.query(User).filter_by(age=30).all()
for user in users:
    print(f"User: {user.name}, Age: {user.age}")


name = 'john_doe'  # Replace with the username you're searching for
retrieved_user = session.query(User).filter_by(name='john_doe').first()
if retrieved_user:
    print(f"User Found: {retrieved_user.name}, Age: {retrieved_user.age}")
else:
    print("User not found")