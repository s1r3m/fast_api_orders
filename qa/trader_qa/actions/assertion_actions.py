import allure
from requests import Response

from trader_qa.actions.base_actions import BaseActions
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
