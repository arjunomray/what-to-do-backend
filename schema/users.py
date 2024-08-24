from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$zK.yD.k4wQQFQegxhW/XNeJnQNpAX/GsJXUWTe5sxMGEUMZr8De36",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "$2b$12$PePP7.6YYwm9r5khEIow2uY7RReBOGc/.1KE8hqs1z7411sbdShxy",
        "disabled": True,
    },
}


class UserBase(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDb(UserBase):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDb(**user_dict)
