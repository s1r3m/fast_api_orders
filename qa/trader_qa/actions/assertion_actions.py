import allure
from requests import Response

from trader_qa.actions.base_actions import BaseActions


class AssertionActions(BaseActions):
    @allure.step
    def check_ping_response(self, response: Response) -> None:
        assert response.json() == 'pong'
