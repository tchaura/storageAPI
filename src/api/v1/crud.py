from typing import List, Sequence, Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

from src.api.v1.models import (
    Order,
    OrderItem,
    OrderItemCreate,
    Product,
    ProductCreate,
    ProductUpdate,
)
from src.exceptions import BadRequest


async def get_items(
    item_type: Type[SQLModel], db: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[SQLModel]:
    result = await db.execute(select(item_type).offset(skip).limit(limit))
    return result.scalars().all()


# Product CRUD functions
async def create_product(db: AsyncSession, data: ProductCreate) -> Product:
    product = Product(**data.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def get_products(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[SQLModel]:
    return await get_items(Product, db, skip, limit)


async def get_product(db: AsyncSession, product_id: int) -> Type[Product] | None:
    product = await db.get(Product, product_id)
    return product


async def update_product(
    db: AsyncSession, product_id: int, product_data: ProductUpdate
) -> Type[Product] | None:
    db_product = await get_product(db, product_id)
    for key, value in product_data.model_dump(exclude_unset=True).items():
        setattr(db_product, key, value)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def delete_product(db: AsyncSession, product_id: int) -> Type[Product] | None:
    product = await get_product(db, product_id)
    await db.delete(product)
    await db.commit()
    return product


# Order CRUD functions
async def create_order(db: AsyncSession, items: List[OrderItemCreate]) -> Order:
    order = Order()
    db.add(order)
    await db.commit()

    try:
        for item in items:
            product = await get_product(db, item.product_id)
            if product.stock < item.quantity:
                e = BadRequest(
                    detail="The item quantity is greater than available stock"
                )
                await db.delete(order)
                raise e
            product.stock -= item.quantity  # Decrease stock

            db_order_item = OrderItem(
                order_id=order.id, product_id=product.id, quantity=item.quantity
            )
            db.add(db_order_item)
    finally:
        await db.commit()
    await db.refresh(order)
    return order


async def get_orders(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[SQLModel]:
    return await get_items(Order, db, skip, limit)


async def get_order(db: AsyncSession, order_id: int) -> Type[Order] | None:
    order = await db.get(Order, order_id)
    return order


async def update_order_status(
    db: AsyncSession, order_id: int, status: str
) -> Type[Order] | None:
    order = await get_order(db, order_id)
    order.status = status
    await db.commit()
    await db.refresh(order)
    return order
