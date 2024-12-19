from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from db_models import OrderModel

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


async def broadcast_order_status_update(order: OrderModel) -> None:
    """Broadcast order status updates to all connected WebSocket clients"""
    message = f'Order {order.id} status updated to {order.status}'
    for connection in active_connections:
        await connection.send_text(message)
