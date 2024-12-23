import asyncio
import json
from http import HTTPStatus
from operator import attrgetter, itemgetter

import allure
from pytest import ExceptionInfo
from requests import Response
from websockets.asyncio.client import ClientConnection

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

    @allure.step
    async def check_ws_messages(self, ws_client: ClientConnection, order: Order) -> None:
        received_messages = []
        expected_messages = order.expected_ws_messages()
        allure.attach(json.dumps(expected_messages), 'expected_messages', allure.attachment_type.JSON)
        for _ in expected_messages:
            try:
                message = await ws_client.recv()
                received_messages.append(message)
            except asyncio.TimeoutError as exc:
                raise AssertionError(
                    f'Not enough messages received:\n{received_messages}\n{expected_messages=}'
                ) from exc
        allure.attach(json.dumps(received_messages), 'received_messages', allure.attachment_type.JSON)
        assert received_messages == expected_messages
