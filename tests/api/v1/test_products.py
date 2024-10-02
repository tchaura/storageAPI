import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_product(async_client: AsyncClient):
    # Setup
    product_data = {
        "name": "Test Product",
        "description": "A sample product",
        "price": 10.5,
        "stock": 100,
    }

    # Execution
    response = await async_client.post("/products", json=product_data)

    # Verification
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["price"] == product_data["price"]
    assert data["stock"] == product_data["stock"]

    # Teardown
    await async_client.delete(f"/products/{data['id']}")


@pytest.mark.asyncio
async def test_get_products(async_client: AsyncClient):
    # Setup
    product1_data = {
        "name": "Product 1",
        "description": "First product",
        "price": 5.0,
        "stock": 50,
    }
    product2_data = {
        "name": "Product 2",
        "description": "Second product",
        "price": 15.0,
        "stock": 30,
    }
    product1 = await async_client.post("/products", json=product1_data)
    product2 = await async_client.post("/products", json=product2_data)

    # Execution
    response = await async_client.get("/products")

    # Verification
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # Teardown
    await async_client.delete(f"/products/{product1.json()['id']}")
    await async_client.delete(f"/products/{product2.json()['id']}")


@pytest.mark.asyncio
async def test_get_product(async_client: AsyncClient):
    # Setup
    product_data = {
        "name": "Single Product",
        "description": "A product",
        "price": 20.0,
        "stock": 40,
    }
    create_response = await async_client.post("/products", json=product_data)
    product_id = create_response.json()["id"]

    # Execution
    response = await async_client.get(f"/products/{product_id}")

    # Verification
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]

    # Teardown
    await async_client.delete(f"/products/{product_id}")


@pytest.mark.asyncio
async def test_update_product(async_client: AsyncClient):
    # Setup
    product_data = {
        "name": "Old Product",
        "description": "Outdated",
        "price": 10.0,
        "stock": 10,
    }
    create_response = await async_client.post("/products", json=product_data)
    product_id = create_response.json()["id"]

    # Execution
    updated_data = {
        "name": "Updated Product",
        "description": "Updated description",
        "price": 12.0,
        "stock": 20,
    }
    response = await async_client.put(f"/products/{product_id}", json=updated_data)

    # Verification
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["price"] == updated_data["price"]

    # Teardown
    await async_client.delete(f"/products/{product_id}")


@pytest.mark.asyncio
async def test_delete_product(async_client: AsyncClient):
    # Setup
    product_data = {
        "name": "To be deleted",
        "description": "Sample",
        "price": 10.0,
        "stock": 10,
    }
    create_response = await async_client.post("/products", json=product_data)
    product_id = create_response.json()["id"]

    # Execution
    delete_response = await async_client.delete(f"/products/{product_id}")

    # Verification
    assert delete_response.status_code == 200
    verify_response = await async_client.get(f"/products/{product_id}")
    assert verify_response.status_code == 404
