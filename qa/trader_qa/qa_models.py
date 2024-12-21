from dataclasses import dataclass, field

from trader_qa.constants import OrderStatus


@dataclass(slots=True)
class Order:
    stocks: str
    quantity: int
    status: OrderStatus = OrderStatus.PENDING
    id: int = 0  # Temp value

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def from_order(cls, order: 'Order') -> 'Order':
        return Order(stocks=order.stocks, quantity=order.quantity)


@dataclass(slots=True)
class Repositories:
    orders: set[Order] = field(default_factory=set)
