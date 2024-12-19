from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db import get_db
from db_models import OrderModel
from models import Order, OrderResponse

router = APIRouter()


@router.get('/ping')
async def ping() -> str:
    """Simple ping endpoint to test the API"""
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
    result = await db.execute(select(OrderModel).where(OrderModel.status != OrderModel.OrderStatus.CANCELED))
    orders = result.scalars().all()

    return [OrderResponse.model_validate(order) for order in orders]


@router.post(
    '/orders',
    status_code=HTTPStatus.CREATED,
    response_model=OrderResponse,
    responses={
        201: {'description': 'Order placed'},
        400: {'description': 'Invalid input'},
    },
)
async def create_order(order: Order, db: AsyncSession = Depends(get_db)) -> OrderResponse | JSONResponse:
    """Create a new order"""
    try:
        db_order = OrderModel(stocks=order.stocks, quantity=order.quantity, status=OrderModel.OrderStatus.PENDING)
        db.add(db_order)
        await db.commit()

        return OrderResponse.model_validate(db_order)
    except ValueError as e:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content=str(e))


@router.get(
    '/orders/{order_id}',
    response_model=OrderResponse,
    responses={
        200: {'description': 'Order found'},
        404: {'description': 'Order not found'},
    },
)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)) -> OrderResponse | JSONResponse:
    """Get an order by id"""
    try:
        order = await db.get(OrderModel, order_id)
        if not order:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Order {order_id} not found!')

        return OrderResponse.model_validate(order)
    except ValueError as e:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content=str(e))


@router.delete(
    '/orders/{order_id}',
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        204: {'description': 'Order canceled'},
        404: {'description': 'Order not found'},
    },
)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)) -> None:  # pylint: disable=unused-argument
    """Cancel an order by id"""
    try:
        order = await db.get(OrderModel, order_id)
        if not order:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Order {order_id} not found!')

        order.status = OrderModel.OrderStatus.CANCELED
        await db.refresh(order)
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
