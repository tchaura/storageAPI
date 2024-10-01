from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


# Order status enum
class OrderStatus(str, Enum):
    in_process = "in process"
    sent = "sent"
    delivered = "delivered"


# Product models
class ProductBase(SQLModel):
    name: str = Field(nullable=False, min_length=5, max_length=255)
    description: Optional[str] = Field(default=None)
    price: float = Field(ge=0)
    stock: int = Field(ge=0)


class ProductRead(ProductBase):
    id: int


class ProductCreate(ProductBase): ...


class ProductUpdate(ProductBase): ...


class Product(ProductBase, table=True):
    __tablename__ = "products"

    id: int = Field(primary_key=True)


# Order item models
class OrderItemBase(SQLModel):
    quantity: int = Field(gt=0)
    product_id: int = Field(foreign_key="products.id")


class OrderItemRead(OrderItemBase): ...


class OrderItemCreate(OrderItemBase): ...


# Order Item models
class OrderItem(OrderItemBase, table=True):
    __tablename__ = "order_items"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique identifier for the order item",
    )
    order_id: int = Field(
        foreign_key="orders.id", description="ID of the order this item belongs to"
    )

    order: "Order" = Relationship(
        back_populates="items", sa_relationship_kwargs={"lazy": "selectin"}
    )
    product: Product = Relationship(sa_relationship_kwargs={"lazy": "selectin"})


# Order models
class OrderBase(SQLModel):
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    status: OrderStatus = Field(default=OrderStatus.in_process)


class OrderCreate(SQLModel):
    items: List[OrderItemCreate]


class OrderRead(OrderBase):
    items: List[OrderItemRead]


class Order(OrderBase, table=True):
    __tablename__ = "orders"
    items: List[OrderItem] = Relationship(
        back_populates="order", sa_relationship_kwargs={"lazy": "selectin"}
    )


class OrderStatusUpdate(SQLModel):
    status: OrderStatus

