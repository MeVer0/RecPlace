import datetime

from typing import Annotated

from fastapi_users.db import SQLAlchemyBaseUserTable

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


intpk = Annotated[int, mapped_column(primary_key=True)]


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[intpk]
    email: Mapped[str]
    username: Mapped[str]
    hashed_password: Mapped[str]
    is_active: Mapped[bool]
    is_superuser: Mapped[bool]
    is_verified: Mapped[bool]


class UserRequestLog(Base):
    __tablename__ = "user_request_log"

    req_id: Mapped[intpk]
    user_id: Mapped[int]
    req_text: Mapped[str]
    date_create: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
