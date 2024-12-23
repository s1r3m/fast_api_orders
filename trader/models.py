from pydantic import BaseModel, Field

from db import OrderModel


class OrderInput(BaseModel):
    stocks: str
    quantity: int = Field(gt=0, description='The quantity must be more than 0.')


class OrderResponse(BaseModel):
    id: int
    stocks: str
    quantity: int
    status: OrderModel.OrderStatus

    class Config:
        from_attributes = True


class CreateOrderResponse(BaseModel):
    id: int
    status: OrderModel.OrderStatus

    class Config:
        from_attributes = True
