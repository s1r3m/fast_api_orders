import pytest

from trader_qa.constants import OrderStatus


@pytest.mark.usefixtures('not_created_order')
def test_get_all_orders__no_orders__empty_response(actions):
    response = actions.user.get_all_orders()
    actions.assertion.check_all_orders_response(response)


def test_get_all_orders__mixed_orders__orders_in_response(actions, cancelled_order, pending_order):
    response = actions.user.get_all_orders()
    actions.assertion.check_all_orders_response(response, pending_order, cancelled_order)


def test_get_all_orders__executed_orders__orders_in_response(actions, pending_order, executed_order):
    response = actions.user.get_all_orders()

    pending_order.status = OrderStatus.EXECUTED  # Due to delay nature this order will be executed, too
    actions.assertion.check_all_orders_response(response, pending_order, executed_order)
