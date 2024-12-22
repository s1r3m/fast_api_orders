from http import HTTPStatus

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db import get_db, OrderModel
from logic import execute_order
from models import CreateOrderResponse, OrderInput, OrderResponse
from web_socket import broadcast_order_status_update

router = APIRouter()


@router.get('/ping')
async def ping() -> str:
    """Simple ping endpoint to test the app."""
    return 'pong'


@router.get(
    '/orders',
    response_model=list[OrderResponse],
    responses={
        200: {'description': 'A list of orders'},
    },
)
async def get_orders(db: AsyncSession = Depends(get_db)) -> list[OrderResponse]:
    """Get all orders"""
    result = await db.execute(select(OrderModel))
    orders = result.scalars().all()

    return [OrderResponse.model_validate(order) for order in orders]


@router.post(
    '/orders',
    status_code=HTTPStatus.CREATED,
    response_model=CreateOrderResponse,
    responses={
        201: {'description': 'Order placed'},
        400: {'description': 'Invalid input'},
    },
)
async def create_order(
    order: OrderInput, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)
) -> CreateOrderResponse:
    """Create a new order"""
    new_order = OrderModel(stocks=order.stocks, quantity=order.quantity, status=OrderModel.OrderStatus.PENDING)
    async with db.begin():
        db.add(new_order)

    background_tasks.add_task(execute_order, new_order.id)
    await broadcast_order_status_update(new_order.id, new_order.status)

    return OrderResponse.model_validate(new_order)


@router.get(
    '/orders/{order_id}',
    response_model=OrderResponse,
    responses={
        200: {'description': 'Order found'},
        404: {'description': 'Order not found'},
    },
)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)) -> OrderResponse:
    """Get an order by id"""
    order = await db.get(OrderModel, order_id)
    if not order:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Order {order_id} not found!')

    return OrderResponse.model_validate(order)


@router.delete(
    '/orders/{order_id}',
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        204: {'description': 'Order canceled'},
        404: {'description': 'Order not found'},
    },
)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)) -> None:
    """Cancel an order by id"""
    order = await db.get(OrderModel, order_id)
    if not order:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Order {order_id} not found!')

    if order.status != OrderModel.OrderStatus.PENDING:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=f'Order {order_id} cannot be cancelled!')

    order.status = OrderModel.OrderStatus.CANCELLED
    await db.commit()

    await broadcast_order_status_update(order.id, order.status)
