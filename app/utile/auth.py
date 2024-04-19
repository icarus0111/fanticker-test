from http.client import HTTPException
from fastapi import HTTPException, status

from fastapi.security import HTTPBasicCredentials

from app.main import pwd_context

users = {
    "user1": {
        "username": "user1",
        "password": pwd_context.hash("password1"),
        "disabled": False,
        "roles": ["counter-reader"]
    },
    "user2": {
        "username": "user2",
        "password": pwd_context.hash("password2"),
        "disabled": False,
        "roles": ["counter-incrementer"]
    }
}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(credentials: HTTPBasicCredentials):
    user = users.get(credentials.username)
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return user
