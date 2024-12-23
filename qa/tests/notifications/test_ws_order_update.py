import asyncio
from asyncio import sleep

import pytest_asyncio
from websockets import connect
from websockets.asyncio.client import ClientConnection

from settings import HOST
from trader_qa.constants import ORDER_EXECUTE_DELAY, WS_TIMEOUT
from trader_qa.qa_models import Order

WS_URL = f'ws://{HOST}/ws'


@pytest_asyncio.fixture
async def ws_client_messages() -> asyncio.Queue:
    async with connect(WS_URL, open_timeout=WS_TIMEOUT) as websocket:
        queue: asyncio.Queue = asyncio.Queue()

        async def receive_messages():
            try:
                while True:
                    message = await asyncio.wait_for(websocket.recv(), WS_TIMEOUT)
                    await queue.put(message)
            except asyncio.TimeoutError:
                print('No message received')
                pass

        receive_task = asyncio.create_task(receive_messages())

        yield queue

        receive_task.cancel()


@pytest_asyncio.fixture
async def ws_client_2() -> ClientConnection:
    async with connect(WS_URL, open_timeout=WS_TIMEOUT) as websocket:
        yield websocket


async def test_ws__order_created__msg_received(actions, ws_client_messages):
    order = Order()
    actions.user.create_order(order)
    await actions.assertion.check_ws_messages(ws_client_messages, order)


async def test_ws__order_cancelled__msg_received_in_right_order(actions, ws_client_messages):
    order = Order()
    actions.user.create_order(order)

    actions.user.cancel_order(order)

    await actions.assertion.check_ws_messages(ws_client_messages, order)


async def test_ws__order_executed__msg_received_in_right_order(actions, ws_client_messages):
    order = Order()
    actions.user.create_order(order)

    await sleep(ORDER_EXECUTE_DELAY)

    await actions.assertion.check_ws_messages(ws_client_messages, order)


# async def test_ws__two_clients__all_clients_received_messages(actions, ws_client_1, ws_client_2):
#     order = Order()
#     actions.user.create_order(order)
#
#     actions.user.cancel_order(order)
#
#     await actions.assertion.check_ws_messages(ws_client_1, order)
#     await actions.assertion.check_ws_messages(ws_client_2, order)
