from http import HTTPStatus

import pytest
from pytest_lazy_fixtures import lf as lazy_fixture

from trader_qa.clients.api_client import UnexpectedStatusCode
from trader_qa.constants import Error, OrderStatus
from trader_qa.qa_models import Order


def test_cancel_order__pending_order__order_cancelled(actions, pending_order):
    actions.user.cancel_order(pending_order)

    pending_order.status = OrderStatus.CANCELLED
    actions.assertion.check_order(pending_order)


@pytest.mark.parametrize(
    'order',
    [
        lazy_fixture('executed_order'),
        lazy_fixture('cancelled_order'),
    ],
)
def test_cancel_order__not_pending_order__error_response(actions, order):
    status_before = order.status
    with pytest.raises(UnexpectedStatusCode) as exc:
        actions.user.cancel_order(order)

    order.status = status_before
    actions.assertion.check_order(order)  # Check the order is not modified
    actions.assertion.check_error_response(
        exc, Error.ORDER_CANNOT_BE_CANCELLED_TPL.format(order_id=order.id), HTTPStatus.CONFLICT
    )


@pytest.mark.usefixtures('pending_order')
def test_cancel_order__not_existent_order__error_response(actions, not_created_order):
    with pytest.raises(UnexpectedStatusCode) as exc:
        actions.user.cancel_order(not_created_order)

    actions.assertion.check_error_response(
        exc, Error.ORDER_NOT_FOUND_TPL.format(order_id=not_created_order.id), HTTPStatus.NOT_FOUND
    )


def test_cancel_order__bad_order_id__error_response(actions):
    bad_order = Order(id='bad')

    with pytest.raises(UnexpectedStatusCode) as exc:
        actions.user.cancel_order(bad_order)

    actions.assertion.check_error_response(exc, Error.SHOULD_BE_VALID_INTEGER, HTTPStatus.UNPROCESSABLE_ENTITY)
