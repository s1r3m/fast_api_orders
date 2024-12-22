from trader_qa.actions.assertion_actions import AssertionActions
from trader_qa.actions.user_actions import UserActions
from trader_qa.clients import Clients
from trader_qa.qa_models import Repositories


class TraderActions:
    def __init__(self) -> None:
        self._clients = Clients()
        self._repositories = Repositories()

        self.user = UserActions(self._clients, self._repositories)
        self.assertion = AssertionActions(self._clients, self._repositories)

    def cleanup(self) -> None:
        for order in self._repositories.orders:
            self._clients.db.delete_order(order.id)
        self._clients.db.check_db_isolation()
