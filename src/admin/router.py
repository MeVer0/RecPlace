from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import aliased

from src.database import async_session_maker
from src.auth.auth_backend import fastapi_users


from src.models import User, UserRequestLog

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(fastapi_users.current_user(active=True, superuser=True))]
)


@router.get("/get_users")
async def get_users():
    """
    Получаем всех пользователей
    """

    async with async_session_maker() as session:
        users = await session.execute(select(User.email, User.username, User.is_verified).select_from(User).where(User.is_superuser is not True))

        return [row._asdict() for row in users]


@router.get("/get_user_requests")
async def get_user_requests(user_id: int):
    """
    :param user_id id пользователя

    Получаем запросы пользователя по его id
    """

    URL = aliased(UserRequestLog)

    async with async_session_maker() as session:
        user_request_log = await session.execute(select(URL.user_id, URL.req_text, URL.date_create).select_from(URL).where(URL.user_id == user_id))

        return [row._asdict() for row in user_request_log]