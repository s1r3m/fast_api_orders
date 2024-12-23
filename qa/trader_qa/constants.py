from enum import Enum

WS_TIMEOUT = 5


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
    RUREUR = 'RUREUR'
    NOT_EXISTING = 'NOT_EXISTING'


class Table(StrEnum):
    ORDERS = 'orders'


class Error(StrEnum):
    GREATER_THAN_0 = 'Input should be greater than 0'
    ORDER_CANNOT_BE_CANCELLED_TPL = 'Order {order_id} cannot be cancelled!'
    ORDER_NOT_FOUND_TPL = 'Order {order_id} not found!'
    SHOULD_BE_VALID_INTEGER = 'Input should be a valid integer, unable to parse string as an integer'
    STOCK_NOT_EXISTING = 'Stocks is not of valid value'
