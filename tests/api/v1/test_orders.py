import pytest
from httpx import AsyncClient


@pytest.mark.asyncio()
async def test_create_order(async_client: AsyncClient):
    # Setup
    product_data = {"name": "Order Product", "price": 50.0, "stock": 20}
    product_response = await async_client.post("/products", json=product_data)
    product_id = product_response.json()["id"]

    # Execution
    order_data = {"items": [{"product_id": product_id, "quantity": 2}]}
    response = await async_client.post("/orders", json=order_data)

    # Verification
    assert response.status_code == 201
    order = response.json()
    assert len(order["items"]) == 1
    assert order["items"][0]["product_id"] == product_id

    # Teardown
    await async_client.delete(f"/orders/{order['id']}")
    await async_client.delete(f"/products/{product_id}")


@pytest.mark.asyncio
async def test_get_orders(async_client: AsyncClient):
    # Setup
    product_data = {"name": "Product for order", "price": 50.0, "stock": 20}
    product_response = await async_client.post("/products", json=product_data)
    product_id = product_response.json()["id"]
    order_data = {"items": [{"product_id": product_id, "quantity": 1}]}
    order_response = await async_client.post("/orders", json=order_data)

    # Execution
    response = await async_client.get("/orders")

    # Verification
    assert response.status_code == 200
    orders = response.json()
    assert len(orders) >= 1

    # Teardown
    await async_client.delete(f"/orders/{order_response.json()['id']}")
    await async_client.delete(f"/products/{product_id}")


@pytest.mark.asyncio
async def test_get_order_by_id(async_client: AsyncClient):
    # Setup
    product_data = {"name": "Order product", "price": 50.0, "stock": 20}
    product_response = await async_client.post("/products", json=product_data)
    product_id = product_response.json()["id"]
    order_data = {"items": [{"product_id": product_id, "quantity": 1}]}
    order_response = await async_client.post("/orders", json=order_data)
    order_id = order_response.json()["id"]

    # Execution
    response = await async_client.get(f"/orders/{order_id}")

    # Verification: Verify the order details
    assert response.status_code == 200
    order = response.json()
    assert order["id"] == order_id

    # Teardown
    await async_client.delete(f"/orders/{order_id}")
    await async_client.delete(f"/products/{product_id}")


@pytest.mark.asyncio
async def test_update_order_status(async_client: AsyncClient):
    # Setup
    product_data = {"name": "Order product", "price": 50.0, "stock": 20}
    product_response = await async_client.post("/products", json=product_data)
    product_id = product_response.json()["id"]
    order_data = {"items": [{"product_id": product_id, "quantity": 1}]}
    order_response = await async_client.post("/orders", json=order_data)
    order_id = order_response.json()["id"]

    # Execution
    update_data = {"status": "sent"}
    response = await async_client.patch(f"/orders/{order_id}/status", json=update_data)

    # Verification
    assert response.status_code == 200
    updated_order = response.json()
    assert updated_order["status"] == "sent"

    # Teardown
    await async_client.delete(f"/orders/{order_id}")
    await async_client.delete(f"/products/{product_id}")
