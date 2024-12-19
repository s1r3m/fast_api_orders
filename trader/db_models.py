from enum import Enum

from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import Column, Enum as SqlEnum, Integer, String

Base: DeclarativeMeta = declarative_base()


class StrEnum(str, Enum):
    """A class where all values are also strings."""


class OrderModel(Base):
    __tablename__ = 'orders'

    class OrderStatus(StrEnum):
        CANCELED = 'CANCELED'
        EXECUTED = 'EXECUTED'
        PENDING = 'PENDING'

    id = Column(Integer, primary_key=True, index=True)
    stocks = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(SqlEnum(OrderStatus, name='OrderStatus'), nullable=False)
