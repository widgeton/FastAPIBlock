from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from typing import Annotated
from datetime import datetime

from config import settings

async_engine = create_async_engine(url=settings.DB_URL)
async_session_factory = async_sessionmaker(bind=async_engine, autoflush=False)

pk = Annotated[int, mapped_column(primary_key=True, nullable=False, unique=True, autoincrement=True)]

crated_dt = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_dt = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                               onupdate=text("TIMEZONE('utc', now())"))]


class Base(DeclarativeBase):
    pass
