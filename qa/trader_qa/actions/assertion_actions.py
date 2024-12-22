from http import HTTPStatus
from operator import attrgetter, itemgetter

import allure
from py._code.code import ExceptionInfo
from requests import Response

from trader_qa.actions.base_actions import BaseActions
from trader_qa.constants import Error
from trader_qa.qa_models import Order


class AssertionActions(BaseActions):
    @allure.step
    def check_ping_response(self, response: Response) -> None:
        assert response.json() == 'pong'

    @allure.step
    def check_order(self, order: Order, response: Response | None = None) -> None:
        if response is None:
            response = self._clients.api.get_order(order.id)

        assert response.json() == {
            'id': order.id,
            'stocks': order.stocks,
            'quantity': order.quantity,
            'status': order.status,
        }

    @allure.step
    def check_create_order_response(self, response: Response, order: Order) -> None:
        assert response.json() == {
            'id': order.id,
            'status': order.status,
        }

    @allure.step
    def check_error_response(self, exc: ExceptionInfo, error: Error, status_code: HTTPStatus) -> None:
        assert f'but was {status_code}' in str(exc.value)
        assert error in str(exc.value)

    @allure.step
    def check_all_orders_response(self, response: Response, *orders: Order) -> None:
        body = response.json()
        sorted_orders = sorted(body, key=itemgetter('id'))
        sorted_expected_orders = sorted(orders, key=attrgetter('id'))

        got_orders = len(sorted_orders)
        expected_orders = len(sorted_expected_orders)
        assert got_orders == expected_orders, f'Order count mismatch: {got_orders=}, {expected_orders=}'

        for order, expected_order in zip(sorted_orders, sorted_expected_orders):
            assert order == {
                'id': expected_order.id,
                'stocks': expected_order.stocks,
                'quantity': expected_order.quantity,
                'status': expected_order.status,
            }
