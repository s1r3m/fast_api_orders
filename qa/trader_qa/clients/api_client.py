from http import HTTPStatus

import allure
from requests import Request, RequestException, Response, Session


class UnexpectedStatusCode(RequestException):
    pass


def _truncate_text(text: str) -> str:
    """
    :param text: The response.text value.
    :return: The value of last string response.text if content is not html.
    """
    text = text.strip()
    if not text or text.startswith('<html>'):
        return ''
    return text.split('\n')[-1]


class ApiClient:
    def __init__(self, api_url: str) -> None:
        self._base_url = api_url
        self._session: Session | None = None

    @property
    def session(self) -> Session:
        if self._session is None:
            self._session = Session()
        return self._session

    def _call(self, request: Request, expected_status_code: HTTPStatus) -> Response:
        request.url = self._base_url + request.url

        prepared_request = self.session.prepare_request(request)
        response = self.session.send(prepared_request, verify=False)
        response.request = request  # type: ignore

        if response.status_code != expected_status_code:
            err_msg = (
                f'Expected status code {expected_status_code}, '
                f'but was {response.status_code}.\n{_truncate_text(response.text)}'
            )
            raise UnexpectedStatusCode(err_msg, response=response)

        return response

    @allure.step
    def get_ping(self) -> Response:
        request = Request(
            method='GET',
            url='/ping',
        )
        return self._call(request, HTTPStatus.OK)

    @allure.step
    def post_order(self, stocks: str, quantity: int) -> Response:
        request = Request(
            method='POST',
            url='/orders',
            json={'stocks': stocks, 'quantity': quantity},
            headers={'Content-Type': 'application/json'},
        )
        return self._call(request, HTTPStatus.CREATED)

    @allure.step
    def get_order(self, order_id: int) -> Response:
        request = Request(
            method='GET',
            url=f'/orders/{order_id}',
        )
        return self._call(request, HTTPStatus.OK)
