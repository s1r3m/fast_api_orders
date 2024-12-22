from trader_qa.clients import Clients
from trader_qa.qa_models import Repositories


class BaseActions:
    def __init__(self, clients: Clients, repositories: Repositories) -> None:
        self._clients = clients
        self._repositories = repositories
