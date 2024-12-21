import allure
from requests import Response

from trader_qa.actions.base_actions import BaseActions
from trader_qa.qa_models import Order


class UserActions(BaseActions):
    @allure.step
    def get_ping(self) -> Response:
        return self._clients.api.get_ping()

    @allure.step
    def get_order(self, order: Order) -> Response:
        return self._clients.api.get_order(order.id)

    @allure.step
    def create_order(self, order: Order) -> Response:
        response = self._clients.api.post_order(order.stocks, order.quantity)
        body = response.json()
        order.id = body['id']
        self._repositories.orders.add(order)

        return response
