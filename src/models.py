# models.py

class UserModel:
    # Simulating a database with a dictionary
    users = {"admin": "admin", "user": "user"}

    @staticmethod
    def authenticate(username, password):
        """Validate user credentials."""
        if username in UserModel.users and UserModel.users[username] == password:
            return True
        return False