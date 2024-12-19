from enum import Enum as PyEnum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import DeclarativeMeta

Base: DeclarativeMeta = declarative_base()


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
