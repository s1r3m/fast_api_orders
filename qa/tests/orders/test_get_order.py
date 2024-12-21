from http import HTTPStatus

import pytest

from trader_qa.clients.api_client import UnexpectedStatusCode
from trader_qa.constants import Error
from trader_qa.qa_models import Order


@pytest.mark.parametrize(
    'order',
    [
        pytest.lazy_fixture('pending_order'),
        pytest.lazy_fixture('executed_order'),
        pytest.lazy_fixture('cancelled_order'),
    ],
)
def test_get_order__order_in_db__order_in_response(actions, order):
    response = actions.user.get_order(order)
    actions.assertion.check_order(order, response)


def test_get_order__not_existing_order__error_response(actions, not_created_order):
    with pytest.raises(UnexpectedStatusCode) as exc:
        actions.user.get_order(not_created_order)

    actions.assertion.check_error_response(
        exc, Error.ORDER_NOT_FOUND_TPL.format(order_id=not_created_order.id), HTTPStatus.NOT_FOUND
    )


def test_get_order__bad_order_id__error_response(actions):
    bad_order = Order(id='bad')

    with pytest.raises(UnexpectedStatusCode) as exc:
        actions.user.get_order(bad_order)

    actions.assertion.check_error_response(exc, Error.SHOULD_BE_VALID_INTEGER, HTTPStatus.UNPROCESSABLE_ENTITY)
