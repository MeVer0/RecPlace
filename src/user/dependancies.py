from fastapi import Depends

from src.auth.auth_backend import fastapi_users
from src.models import User


def get_current_user_id(user: User = Depends(fastapi_users.current_user())):
    if user.id:
        user_id = user.id
    else:
        user_id = None
    return user_id