from time import sleep
from typing import Generator, TypeVar

import pytest

from trader_qa.actions import TraderActions
from trader_qa.constants import ORDER_EXECUTE_DELAY, OrderStatus, Stock
from trader_qa.qa_models import Order

T = TypeVar('T')
YieldFixture = Generator[T, None, None]


@pytest.fixture
def actions() -> YieldFixture[TraderActions]:
    _actions = TraderActions()
    yield _actions
    _actions.cleanup()


@pytest.fixture
def pending_order(actions: TraderActions) -> Order:
    order = Order(stocks=Stock.EURUSD, quantity=100)
    actions.user.create_order(order)

    return order


@pytest.fixture
def executed_order(actions: TraderActions) -> Order:
    order = Order(stocks=Stock.EURUSD, quantity=500)
    actions.user.create_order(order)
    sleep(ORDER_EXECUTE_DELAY)

    order.status = OrderStatus.EXECUTED
    return order


@pytest.fixture
def cancelled_order(actions: TraderActions) -> Order:
    order = Order(stocks=Stock.USDEUR, quantity=100500)
    actions.user.create_order(order)
    actions.user.cancel_order(order)

    return order


@pytest.fixture
def not_created_order() -> Order:
    order = Order(id=123, stocks=Stock.USDEUR, quantity=1)

    return order
