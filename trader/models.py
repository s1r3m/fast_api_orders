from pydantic import BaseModel, Field


class Order(BaseModel):
    stocks: str
    quantity: int = Field(ge=0, description='The quantity must be more than 0.')


class OrderResponse(BaseModel):
    stocks: str
    quantity: int

    class Config:
        from_attributes = True
