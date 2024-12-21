from http import HTTPStatus

import pytest

from trader_qa.clients.api_client import UnexpectedStatusCode
from trader_qa.constants import Error, Stock
from trader_qa.qa_models import Order


def test_create_order__valid_data__order_created(actions):
    order = Order(stocks=Stock.EURUSD, quantity=10)

    response = actions.user.create_order(order)

    actions.assertion.check_create_order_response(response, order)
    actions.assertion.check_order(order)


@pytest.mark.usefixtures('pending_order')
def test_create_order__second_order__order_created(actions):
    new_order = Order(stocks=Stock.USDEUR, quantity=100)

    response = actions.user.create_order(new_order)

    actions.assertion.check_create_order_response(response, new_order)
    actions.assertion.check_order(new_order)


@pytest.mark.parametrize(
    'order',
    [
        pytest.lazy_fixture('pending_order'),
        pytest.lazy_fixture('executed_order'),
        pytest.lazy_fixture('cancelled_order'),
    ],
)
def test_create_order__same_data__order_created(actions, order):
    same_data_order = Order.from_order(order)

    response = actions.user.create_order(same_data_order)

    actions.assertion.check_create_order_response(response, same_data_order)
    actions.assertion.check_order(same_data_order)


@pytest.mark.parametrize(
    'quantity',
    [
        pytest.param(0, id='zero_value'),
        pytest.param(-1, id='negative_value'),
    ],
)
def test_create_order__bad_quantity__error_response(actions, quantity):
    order = Order(stocks=Stock.EURUSD, quantity=quantity)

    with pytest.raises(UnexpectedStatusCode) as exc:
        actions.user.create_order(order)

    actions.assertion.check_error_response(exc, Error.GREATER_THAN_0, HTTPStatus.UNPROCESSABLE_ENTITY)


def test_create_order__bad_type_quantity__error_response(actions):
    bad_order = Order(quantity='bad')

    with pytest.raises(UnexpectedStatusCode) as exc:
        actions.user.create_order(bad_order)

    actions.assertion.check_error_response(exc, Error.SHOULD_BE_VALID_INTEGER, HTTPStatus.UNPROCESSABLE_ENTITY)


@pytest.mark.skip(reason='not_implemented_task_DAY-12')
def test_create_order__bad_stock__error_response(actions):
    order = Order(stocks=Stock.NOT_EXISTING, quantity=111)

    with pytest.raises(UnexpectedStatusCode) as exc:
        actions.user.create_order(order)

    actions.assertion.check_error_response(exc, Error.STOCK_NOT_EXISTING, HTTPStatus.BAD_REQUEST)
