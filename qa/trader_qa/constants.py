from enum import Enum


class StrEnum(str, Enum):
    """Enum where every value is also a string."""


# From the app.
ORDER_EXECUTE_DELAY = 2


class OrderStatus(StrEnum):
    CANCELLED = 'CANCELLED'
    EXECUTED = 'EXECUTED'
    PENDING = 'PENDING'


class Stock(StrEnum):
    EURUSD = 'EURUSD'
    USDEUR = 'USDEUR'
    NOT_EXISTING = 'NOT_EXISTING'


class Table(StrEnum):
    ORDERS = 'orders'


class Error(StrEnum):
    GREATER_THAN_0 = 'Input should be greater than 0'
    STOCK_NOT_EXISTING = 'Stocks is not of valid value'
