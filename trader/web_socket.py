from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from db import OrderModel

active_connections: List[WebSocket] = []

ws_router = APIRouter()


@ws_router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket) -> None:
    """WebSocket endpoint to accept client connections"""
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Just to keep the connection alive
    except WebSocketDisconnect:
        active_connections.remove(websocket)


async def broadcast_order_status_update(order_id: int, status: OrderModel.OrderStatus) -> None:
    """Broadcast order status updates to all connected WebSocket clients"""
    message = f'Order {order_id} status updated to {status}'
    for connection in active_connections:
        await connection.send_text(message)
