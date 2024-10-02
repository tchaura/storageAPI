
# Warehouse Management REST API

This project implements a FastAPI-based REST API for managing warehouse processes. The API allows you to manage products, inventory, and orders. It was built with ease of local development in mind and includes configurations for production deployment.

## Features
- **Database with SQLAlchemy (v2)**
  - Designed entities: `Product`, `Order`, and `OrderItem`
  - Async SQLAlchemy engine with pessimistic connection pooling
  - Migration setup using Alembic with migrations formatted for easy sorting (`YYYY-MM-DD_slug`)
  - Global Pydantic model with explicit timezone setting during JSON export
- **Business Logic**
  - Stock checks during order creation to ensure sufficient stock
  - Automatic inventory updates when orders are placed
  - Error handling for insufficient stock
- **API Endpoints**
  - **Product Management**
    - Create Product (POST `/products`)
    - Get List of Products (GET `/products`)
    - Get Product by ID (GET `/products/{id}`)
    - Update Product (PUT `/products/{id}`)
    - Delete Product (DELETE `/products/{id}`)
  - **Order Management**
    - Create Order (POST `/orders`)
    - Get List of Orders (GET `/orders`)
    - Get Order by ID (GET `/orders/{id}`)
    - Update Order Status (PATCH `/orders/{id}/status`)
- **Production-Ready**
  - Configured with Gunicorn and Docker
  - JSON logs, Sentry for error reporting
  - Dockerfile optimized for fast builds and small size
  - Dynamic Gunicorn worker configuration

## Local Development

### Setup
1. Install dependencies:
   - MacOS: `brew install just`
   - Debian/Ubuntu: `apt install just`
   - Others: [link](https://github.com/casey/just?tab=readme-ov-file#packages)
2. Install `poetry`:
   ```shell
   pip install poetry
   ```
   Or follow other installation methods [here](https://python-poetry.org/docs/#installation).
3. Set up PostgreSQL (16.3) and start containers:
   ```shell
   just up
   ```

### Environment Setup
1. Copy the environment file and install dependencies:
   ```shell
   cp .env.example .env
   poetry install
   ```

### Running the API
- Run the server:
   ```shell
   just run
   ```
- With custom logging:
   ```shell
   just run --log-config logging.ini
   ```

### Code Formatting and Linting
- Format code with `ruff`:
   ```shell
   just lint
   ```

### Database Migrations
- Create migrations:
   ```shell
   just mm *migration_name*
   ```
- Apply migrations:
   ```shell
   just migrate
   ```
- Downgrade migrations:
   ```shell
   just downgrade -1
   ```

## Deployment

Deployment is managed via Docker and Gunicorn. The Dockerfile is optimized for small size and fast builds with a non-root user. The number of workers is dynamically set based on CPU cores.

Run the app in production:
```shell
docker compose -f docker-compose.prod.yml up -d --build
```

## Documentation
FastAPI provides built-in interactive API documentation with Swagger/OpenAPI, which can be accessed at `/docs` once the server is running.
