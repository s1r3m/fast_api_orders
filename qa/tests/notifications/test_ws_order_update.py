from time import sleep

import pytest_asyncio
from websockets import connect
from websockets.asyncio.client import ClientConnection

from settings import HOST
from trader_qa.constants import ORDER_EXECUTE_DELAY
from trader_qa.qa_models import Order

WS_URL = f'ws://{HOST}/ws'


@pytest_asyncio.fixture
async def ws_client_1() -> ClientConnection:
    async with connect(WS_URL) as websocket:
        yield websocket


@pytest_asyncio.fixture
async def ws_client_2() -> ClientConnection:
    async with connect(WS_URL) as websocket:
        yield websocket


async def test_ws__order_created__msg_received(actions, ws_client_1):
    order = Order()
    actions.user.create_order(order)
    await actions.assertion.check_ws_messages(ws_client_1, order)


async def test_ws__order_cancelled__msg_received_in_right_order(actions, ws_client_1):
    order = Order()
    actions.user.create_order(order)

    actions.user.cancel_order(order)

    await actions.assertion.check_ws_messages(ws_client_1, order)


async def test_ws__order_executed__msg_received_in_right_order(actions, ws_client_1):
    order = Order()
    actions.user.create_order(order)

    sleep(ORDER_EXECUTE_DELAY)

    await actions.assertion.check_ws_messages(ws_client_1, order)


async def test_ws__two_clients__all_clients_received_messages(actions, ws_client_1, ws_client_2):
    order = Order()
    actions.user.create_order(order)

    actions.user.cancel_order(order)

    await actions.assertion.check_ws_messages(ws_client_1, order)
    await actions.assertion.check_ws_messages(ws_client_2, order)
