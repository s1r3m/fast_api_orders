from enum import Enum


class StrEnum(str, Enum):
    """Enum where every value is also a string."""


# From the app.
ORDER_EXECUTE_DELAY = 1


class OrderStatus(StrEnum):
    CANCELED = 'CANCELED'
    EXECUTED = 'EXECUTED'
    PENDING = 'PENDING'


class Stock(StrEnum):
    EURUSD = 'EURUSD'
    USDEUR = 'USDEUR'


class Table(StrEnum):
    ORDERS = 'orders'
