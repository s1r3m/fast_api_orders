import allure
from requests import Response

from trader_qa.actions.base_actions import BaseActions


class UserActions(BaseActions):
    @allure.step
    def get_ping(self) -> Response:
        return self._clients.api.get_ping()
