from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase

from fastapi import Depends

from src.config import db_user, db_host, db_name, db_password
from src.models import User

DATABASE_URL = f"mysql+aiomysql://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
