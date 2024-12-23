import pytest


@pytest.mark.usefixtures('not_created_order')
def test_get_all_orders__no_orders__empty_response(actions):
    response = actions.user.get_all_orders()
    actions.assertion.check_all_orders_response(response)


def test_get_all_orders__mixed_orders__orders_in_response(actions, executed_order, cancelled_order, pending_order):
    response = actions.user.get_all_orders()
    actions.assertion.check_all_orders_response(response, executed_order, pending_order, cancelled_order)
