from trader_qa.constants import Stock
from trader_qa.qa_models import Order


def test_create_order__valid_data__order_created(actions):
    order = Order(stocks=Stock.EURUSD, quantity=10)

    response = actions.user.create_order(order)

    actions.assertion.check_create_order_response(response, order)
    actions.assertion.check_order(order)
