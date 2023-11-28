from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from src.auth.config import secret

from src.models import User
from src.database import get_user_db

from src.auth.smtp import send_mail

SECRET = secret


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        send_mail(
            destination=user.email,
            subject="Перейдите по ссылке, чтобы завершить регистрацию!",
            content=f""""Ваш токен: http://127.0.0.1:8000/auth/verify?token={token}"""

        )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)