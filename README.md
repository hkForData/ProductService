# ProductService

A lightweight e-commerce **Product microservice** built with Python and Flask.
It exposes a RESTful HTTP API for full product lifecycle management: create,
read, update, delete, search, filter, and stock adjustment.

---

## Project Structure

```
ProductService/
├── app.py                        # Flask application entry point
├── requirements.txt              # Python dependencies
├── models/
│   ├── __init__.py
│   └── product.py                # Product dataclass + validation/serialisation
├── services/
│   ├── __init__.py
│   └── product_service.py        # Business-logic layer (CRUD, search, stock)
├── routes/
│   ├── __init__.py
│   └── product_routes.py         # Flask Blueprint – HTTP handlers
└── tests/
    ├── __init__.py
    ├── test_product_service.py   # Unit tests for the service layer
    └── test_product_routes.py    # Integration tests for HTTP routes
```

---

## Getting Started

### Prerequisites

- Python 3.10+

### Installation

```bash
pip install -r requirements.txt
```

### Running the development server

```bash
python app.py
```

The API is available at `http://localhost:5000/api/products/`.

---

## API Reference

| Method   | Path                               | Description                              |
|----------|------------------------------------|------------------------------------------|
| `GET`    | `/api/products/`                   | List all products (supports filters)     |
| `POST`   | `/api/products/`                   | Create a new product                     |
| `GET`    | `/api/products/<id>`               | Retrieve a single product by UUID        |
| `PUT`    | `/api/products/<id>`               | Update an existing product (partial OK)  |
| `DELETE` | `/api/products/<id>`               | Delete a product                         |
| `PATCH`  | `/api/products/<id>/stock`         | Adjust stock level by a quantity delta   |

### Query Parameters (GET /api/products/)

| Parameter  | Description                                              |
|------------|----------------------------------------------------------|
| `category` | Filter products by category (case-insensitive)           |
| `q`        | Full-text search across `name` and `description` fields  |

### Product schema

```json
{
  "id":          "uuid-v4-string",
  "name":        "Widget Pro",
  "description": "A great widget",
  "price":       9.99,
  "stock":       100,
  "category":    "Widgets",
  "sku":         "WGT-PRO-001"
}
```

---

## Running Tests

```bash
pytest tests/ -v
```

41 tests covering the service layer and HTTP routes.

---

## Code Review Notes

### Strengths
- **Layered architecture** – HTTP concerns (routes) are strictly separated from
  business logic (service) and the data model, making each layer independently
  testable and replaceable.
- **Thorough inline documentation** – every public class, method, and non-obvious
  code block carries a docstring explaining intent, parameters, return values,
  and any caveats.
- **Input validation** – all incoming data is validated before persistence;
  meaningful error messages are surfaced to API clients via HTTP 400 responses.
- **Partial updates** – the `PUT` handler applies only the fields present in the
  request body, so clients do not need to re-send unchanged data.
- **Test isolation** – the `autouse` fixture in `test_product_routes.py` resets
  the service singleton before each test, preventing state bleed between cases.

### Known Limitations / Future Work
- **In-memory store** – `ProductService._products` is a plain dict. Swap it with
  a SQLAlchemy session (or similar) for persistence across restarts.
- **No authentication** – add JWT/OAuth middleware before exposing to the internet.
- **Pagination** – `get_all()` returns every product; add `limit`/`offset` query
  parameters for large catalogues.
- **Full-text search** – the current substring search is O(n); integrate
  Elasticsearch or PostgreSQL `tsvector` for production workloads.
- **Concurrency** – the in-memory dict is not thread-safe; use a proper database
  or add locking when running multiple worker processes.
