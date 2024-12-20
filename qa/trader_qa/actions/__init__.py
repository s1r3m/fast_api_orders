from trader_qa.actions.assertion_actions import AssertionActions
from trader_qa.actions.user_actions import UserActions
from trader_qa.clients import Clients


class TraderActions:
    def __init__(self) -> None:
        self._clients = Clients()

        self.user = UserActions(self._clients)
        self.assertion = AssertionActions(self._clients)

    def cleanup(self) -> None:
        pass
