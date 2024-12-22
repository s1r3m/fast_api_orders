import json
from functools import partial
from http import HTTPStatus
from typing import Any

import allure
from requests import PreparedRequest, Request, RequestException, Response, Session

_pretty_json = partial(json.dumps, ensure_ascii=True, indent=4, sort_keys=True)  # pylint: disable=invalid-name


class UnexpectedStatusCode(RequestException):
    pass


def _dump_request_body(request: PreparedRequest) -> str:
    if request.body is None:
        return ''
    try:
        # request_body = request.body.decode() if isinstance(request.body, bytes) else request.body
        body = _pretty_json(json.loads(request.body))
    except ValueError:
        body = request.body  # type: ignore
    return f'Body:\n{body}\n'


def _dump_response_body(response: Response) -> str:
    try:
        body = _pretty_json(response.json())
    except ValueError:
        body = response.content  # type: ignore
    return f'Body:\n{body}\n'


def _truncate_text(text: str) -> str:
    """
    :param text: The response.text value.
    :return: The value of last string response.text if content is not html.
    """
    text = text.strip()
    if not text or text.startswith('<html>'):
        return ''
    return text.split('\n')[-1]


def attach_response(response: Response, *args: Any, **kwargs: Any) -> None:  # pylint: disable=unused-argument
    # Attach request data.
    request = response.request
    request_dump = ''.join(
        [
            f'Method: {request.method}\n',
            f'Url: "{request.url}"\n',
            f'Headers:\n{_pretty_json(dict(request.headers))}\n',
            _dump_request_body(request),
        ]
    )
    allure.attach(
        request_dump,
        name=f'Request - {request.method} {request.path_url}',
        attachment_type=allure.attachment_type.JSON,
    )

    # Attach response data.
    response_dump = ''.join(
        [
            f'Url: "{response.url}"\n',
            f'Status: {response.status_code} {response.reason}\n',
            f'Headers:\n{_pretty_json(dict(response.headers))}\n',
            _dump_response_body(response),
        ]
    )
    allure.attach(
        response_dump,
        name=f'Response - {response.status_code} {request.path_url}',
        attachment_type=allure.attachment_type.JSON,
    )

    content_type = response.headers.get('Content-Type')
    if content_type and content_type.startswith('text/html'):
        allure.attach(
            response.text,
            name=f'Response (as HTML) - {response.status_code} {request.path_url}',
            attachment_type=allure.attachment_type.HTML,
        )


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

        request.hooks = dict(response=attach_response)

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

    @allure.step
    def delete_order(self, order_id: int) -> Response:
        request = Request(
            method='DELETE',
            url=f'/orders/{order_id}',
        )
        return self._call(request, HTTPStatus.NO_CONTENT)

    @allure.step
    def get_orders(self) -> Response:
        request = Request(
            method='GET',
            url='/orders',
        )
        return self._call(request, HTTPStatus.OK)
