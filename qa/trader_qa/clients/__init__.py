from settings import APP_HOST, DATABASE_URL
from trader_qa.clients.api_client import ApiClient
from trader_qa.clients.db_client import DBClient


class Clients:
    def __init__(self) -> None:
        self.api = ApiClient(APP_HOST)
        self.db = DBClient(DATABASE_URL)
