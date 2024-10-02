from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.crud import (
    create_order,
    create_product,
    delete_product,
    get_order,
    get_orders,
    get_product,
    get_products,
    update_order_status,
    update_product,
)
from src.api.v1.models import (
    OrderCreate,
    OrderRead,
    OrderStatusUpdate,
    ProductCreate,
    ProductRead,
    ProductUpdate,
)
from src.database import get_async_session
from src.exceptions import BadRequest, NotFound

router = APIRouter()


# Product Endpoints
@router.post(
    "/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED
)
async def create_product_endpoint(
    product: ProductCreate, db: AsyncSession = Depends(get_async_session)
):
    created_product = await create_product(db, product)
    return created_product


@router.get("/products", response_model=List[ProductRead])
async def get_products_endpoint(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)
):
    return await get_products(db, skip=skip, limit=limit)


@router.get("/products/{product_id}", response_model=ProductRead)
async def get_product_endpoint(
    product_id: int, db: AsyncSession = Depends(get_async_session)
):
    product = await get_product(db, product_id)
    if not product:
        raise NotFound()
    return product


@router.put("/products/{product_id}", response_model=ProductRead)
async def update_product_endpoint(
    product_id: int,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    product = await get_product(db, product_id)
    if not product:
        raise NotFound()
    updated_product = await update_product(db, product_id, product_data)
    return updated_product


@router.delete("/products/{product_id}", response_model=ProductRead)
async def delete_product_endpoint(
    product_id: int, db: AsyncSession = Depends(get_async_session)
):
    product = await get_product(db, product_id)
    if not product:
        raise NotFound()
    return await delete_product(db, product_id)


# Order Endpoints
@router.post("/orders", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order_endpoint(
    order: OrderCreate, db: AsyncSession = Depends(get_async_session)
):
    return await create_order(db, order.items)


@router.get("/orders", response_model=List[OrderRead])
async def get_orders_endpoint(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)
):
    return await get_orders(db, skip=skip, limit=limit)


@router.get("/orders/{order_id}", response_model=OrderRead)
async def get_order_endpoint(
    order_id: int, db: AsyncSession = Depends(get_async_session)
):
    order = await get_order(db, order_id)
    if not order:
        raise NotFound()
    return order


@router.patch("/orders/{order_id}/status", response_model=OrderRead)
async def update_order_status_endpoint(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    order = await get_order(db, order_id)
    if not order:
        raise NotFound()

    if order.status == status_update.status:
        raise BadRequest()

    updated_order = await update_order_status(db, order_id, status_update.status)
    return updated_order
