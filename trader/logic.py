from asyncio import sleep

from db import OrderModel, get_db
from web_socket import broadcast_order_status_update


async def execute_order(order_id: int) -> None:
    await sleep(5)

    async for db in get_db():
        async with db.begin():
            order = await db.get(OrderModel, order_id)
            if order:
                order.status = OrderModel.OrderStatus.EXECUTED

        await broadcast_order_status_update(order.id, order.status)
