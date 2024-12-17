from model_dto import userDto
from model_dto import RoleEnum


register_list = [
    [
        userDto(username="admin", password="admin_password", email="20240182b@gmail.com", mobile_nr="+32476880256"),
        userDto(username="user", password="user_password", email="20240182b@gmail.com", mobile_nr="+32476880256"), 
    ]
]

login_data =[
    ("admin", "admin_password", True),
    ("admin", "ff", False),
    ("admin", "", False),
    ("user", "user_password", True),
    ("user", "", False),
    ("", "", False)
    ]

# users = [
#     userDto(username="admin",password="admin_password",email="20240182b@gmail.com",mobile_nr="+32476880256",role="admin"),
#     userDto(username="user",password="user_password",email="20240182b@gmail.com",mobile_nr="+32476880256",role="user")
# ]