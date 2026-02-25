"""
tests/test_product_routes.py
-----------------------------
Integration tests for the Flask HTTP routes exposed by product_routes.py.

These tests use Flask's built-in test client so no real HTTP server is needed.

Run with:
    pytest tests/
"""

import sys
import os
import json

# Ensure project root is importable.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from app import app
import routes.product_routes as product_routes_module
from services.product_service import ProductService


@pytest.fixture(autouse=True)
def reset_service():
    """
    Replace the module-level service singleton with a fresh instance before
    each test so that products created in one test do not bleed into another.
    """
    product_routes_module._service = ProductService()
    yield


@pytest.fixture
def client():
    """
    Create a Flask test client with a fresh application context per test.
    'TESTING=True' causes Flask to propagate exceptions rather than returning
    500 responses, which makes failures easier to debug in tests.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def created_product(client):
    """Helper that creates a product and returns the parsed JSON response."""
    payload = {
        "name": "Test Widget",
        "description": "A widget for testing",
        "price": 9.99,
        "stock": 50,
        "category": "Widgets",
    }
    response = client.post(
        "/api/products/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 201
    return response.get_json()


# ---------------------------------------------------------------------------
# POST /api/products/
# ---------------------------------------------------------------------------

class TestCreateProduct:
    def test_create_returns_201(self, client):
        payload = {"name": "Widget", "price": 5.0, "stock": 10, "category": "X"}
        resp = client.post(
            "/api/products/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 201
        body = resp.get_json()
        assert body["name"] == "Widget"
        assert "id" in body

    def test_create_with_missing_name_returns_400(self, client):
        payload = {"price": 5.0}
        resp = client.post(
            "/api/products/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_create_with_no_body_returns_400(self, client):
        resp = client.post("/api/products/", content_type="application/json")
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# GET /api/products/
# ---------------------------------------------------------------------------

class TestListProducts:
    def test_list_empty(self, client):
        resp = client.get("/api/products/")
        assert resp.status_code == 200
        assert resp.get_json() == []

    def test_list_returns_created_product(self, client, created_product):
        resp = client.get("/api/products/")
        assert resp.status_code == 200
        products = resp.get_json()
        assert any(p["id"] == created_product["id"] for p in products)

    def test_list_filters_by_category(self, client, created_product):
        resp = client.get("/api/products/?category=Widgets")
        assert resp.status_code == 200
        assert all(p["category"] == "Widgets" for p in resp.get_json())

    def test_list_search_query(self, client, created_product):
        resp = client.get("/api/products/?q=Widget")
        assert resp.status_code == 200
        assert len(resp.get_json()) >= 1


# ---------------------------------------------------------------------------
# GET /api/products/<id>
# ---------------------------------------------------------------------------

class TestGetProduct:
    def test_get_existing_product(self, client, created_product):
        resp = client.get(f"/api/products/{created_product['id']}")
        assert resp.status_code == 200
        assert resp.get_json()["id"] == created_product["id"]

    def test_get_nonexistent_returns_404(self, client):
        resp = client.get("/api/products/does-not-exist")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# PUT /api/products/<id>
# ---------------------------------------------------------------------------

class TestUpdateProduct:
    def test_update_price(self, client, created_product):
        pid = created_product["id"]
        resp = client.put(
            f"/api/products/{pid}",
            data=json.dumps({"price": 19.99}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert resp.get_json()["price"] == 19.99

    def test_update_nonexistent_returns_404(self, client):
        resp = client.put(
            "/api/products/does-not-exist",
            data=json.dumps({"price": 1.0}),
            content_type="application/json",
        )
        assert resp.status_code == 404

    def test_update_with_invalid_data_returns_400(self, client, created_product):
        pid = created_product["id"]
        resp = client.put(
            f"/api/products/{pid}",
            data=json.dumps({"price": -99}),
            content_type="application/json",
        )
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# DELETE /api/products/<id>
# ---------------------------------------------------------------------------

class TestDeleteProduct:
    def test_delete_existing_returns_204(self, client, created_product):
        pid = created_product["id"]
        resp = client.delete(f"/api/products/{pid}")
        assert resp.status_code == 204

    def test_delete_nonexistent_returns_404(self, client):
        resp = client.delete("/api/products/does-not-exist")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# PATCH /api/products/<id>/stock
# ---------------------------------------------------------------------------

class TestAdjustStock:
    def test_increase_stock(self, client, created_product):
        pid = created_product["id"]
        resp = client.patch(
            f"/api/products/{pid}/stock",
            data=json.dumps({"quantity": 10}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert resp.get_json()["stock"] == 60  # 50 + 10

    def test_insufficient_stock_returns_400(self, client, created_product):
        pid = created_product["id"]
        resp = client.patch(
            f"/api/products/{pid}/stock",
            data=json.dumps({"quantity": -1000}),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_missing_quantity_returns_400(self, client, created_product):
        pid = created_product["id"]
        resp = client.patch(
            f"/api/products/{pid}/stock",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert resp.status_code == 400
