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

    def expected_ws_messages(self) -> list[str]:
        match self.status:
            case OrderStatus.PENDING:
                return [f'Order {self.id} status updated to {OrderStatus.PENDING}']
            case OrderStatus.CANCELLED:
                return [
                    f'Order {self.id} status updated to {OrderStatus.PENDING}'
                    f'Order {self.id} status updated to {OrderStatus.CANCELLED}',
                ]
            case OrderStatus.EXECUTED:
                return [
                    f'Order {self.id} status updated to {OrderStatus.PENDING}'
                    f'Order {self.id} status updated to {OrderStatus.EXECUTED}',
                ]
            case _:
                return []


@dataclass(slots=True)
class Repositories:
    orders: set[Order] = field(default_factory=set)
