from dataclasses import dataclass, field

from trader_qa.constants import OrderStatus, Stock


@dataclass(slots=True)
class Order:
    stocks: Stock = Stock.EURUSD
    quantity: int = 10
    status: OrderStatus | None = OrderStatus.PENDING
    id: int = -1  # Temp value while not created

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def from_order(cls, order: 'Order') -> 'Order':
        return Order(stocks=order.stocks, quantity=order.quantity)


@dataclass(slots=True)
class Repositories:
    orders: set[Order] = field(default_factory=set)
