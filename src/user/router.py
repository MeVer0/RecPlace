from fastapi import APIRouter, Depends, Body
from sqlalchemy import select, insert, delete, func, and_
from sqlalchemy.orm import aliased

from src.database import async_session_maker
from src.auth.auth_backend import fastapi_users

from src.models import UserRequestLog
from src.user.dependancies import get_current_user_id

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(fastapi_users.current_user(active=True))]
)


@router.get("/history")
async def get_history(user_id: int = Depends(get_current_user_id)):
    """
    Пользователь получает свою историю запросов
    """

    async with async_session_maker() as session:
        user_requests_history = await session.execute(select(UserRequestLog).
                                                      select_from(UserRequestLog).
                                                      where(UserRequestLog.user_id == user_id))

        return [row._asdict() for row in user_requests_history]


@router.post("/send_request")
async def send_request(
        req_text: str,
        user_id: int = Depends(get_current_user_id)
):
    """
    :param req_text текст пользовательского запроса

    Сохраняет запрос пользователя в БД. Контролирует кол-во сохраненных запросов (максимум 3).

    """

    insert_req = insert(UserRequestLog).values(req_text=req_text, user_id=user_id)

    # Ужасные запросы. Нужно опитимить или обрабатывать на стороне базы через partition over
    req_subquery = select(func.min(UserRequestLog.req_id)).\
                   select_from(UserRequestLog).\
                   where(UserRequestLog.user_id == user_id).limit(1).subquery()

    count_req = select(func.count(UserRequestLog.req_id)).select_from(UserRequestLog).where(UserRequestLog.user_id == user_id)

    del_excess_req = delete(UserRequestLog).where(UserRequestLog.req_id.in_(req_subquery))

    async with async_session_maker() as session:
        await session.execute(insert_req)
        count_req = await session.execute(count_req)
        if count_req.first()[0] > 3:
            await session.execute(del_excess_req)
        await session.commit()


