from enum import Enum as PyEnum
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker

from settings import DATABASE_URL

Base: DeclarativeMeta = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


class StrEnum(str, PyEnum):
    """A class where all values are also strings."""


class OrderModel(Base):
    __tablename__ = 'orders'

    class OrderStatus(StrEnum):
        CANCELLED = 'CANCELLED'
        EXECUTED = 'EXECUTED'
        PENDING = 'PENDING'

    id = Column(Integer, primary_key=True, index=True)
    stocks = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(Enum(OrderStatus, name='OrderStatus'), nullable=False)
