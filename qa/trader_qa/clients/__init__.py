from settings import APP_HOST
from trader_qa.clients.api_client import ApiClient


class Clients:
    def __init__(self) -> None:
        self.api = ApiClient(APP_HOST)
