"""
tests/test_product_service.py
------------------------------
Unit tests for the ProductService business-logic layer.

Run with:
    pytest tests/
"""

import sys
import os

# Ensure the project root is on the path so that local packages resolve.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from services.product_service import ProductService


@pytest.fixture
def service():
    """Return a fresh ProductService instance for each test."""
    return ProductService()


@pytest.fixture
def sample_data():
    """Minimal valid product payload."""
    return {
        "name": "Test Widget",
        "description": "A widget for testing",
        "price": 9.99,
        "stock": 50,
        "category": "Widgets",
    }


# ---------------------------------------------------------------------------
# create()
# ---------------------------------------------------------------------------

class TestCreate:
    def test_create_returns_product(self, service, sample_data):
        product = service.create(sample_data)
        assert product.name == "Test Widget"
        assert product.price == 9.99
        assert product.stock == 50

    def test_create_assigns_unique_ids(self, service, sample_data):
        p1 = service.create(sample_data)
        p2 = service.create(sample_data)
        # Each product must receive a unique identifier.
        assert p1.id != p2.id

    def test_create_raises_for_empty_name(self, service, sample_data):
        sample_data["name"] = ""
        with pytest.raises(ValueError, match="name must not be empty"):
            service.create(sample_data)

    def test_create_raises_for_negative_price(self, service, sample_data):
        sample_data["price"] = -1.0
        with pytest.raises(ValueError, match="price must be"):
            service.create(sample_data)

    def test_create_raises_for_negative_stock(self, service, sample_data):
        sample_data["stock"] = -5
        with pytest.raises(ValueError, match="stock must be"):
            service.create(sample_data)


# ---------------------------------------------------------------------------
# get_all() / get_by_id()
# ---------------------------------------------------------------------------

class TestRead:
    def test_get_all_empty(self, service):
        assert service.get_all() == []

    def test_get_all_returns_all_products(self, service, sample_data):
        service.create(sample_data)
        service.create({**sample_data, "name": "Widget Lite"})
        assert len(service.get_all()) == 2

    def test_get_all_filters_by_category(self, service, sample_data):
        service.create(sample_data)  # category = "Widgets"
        service.create({**sample_data, "name": "Gadget", "category": "Gadgets"})
        widgets = service.get_all(category="Widgets")
        assert len(widgets) == 1
        assert widgets[0].category == "Widgets"

    def test_get_all_category_case_insensitive(self, service, sample_data):
        service.create(sample_data)
        result = service.get_all(category="widgets")  # lower-case lookup
        assert len(result) == 1

    def test_get_by_id_found(self, service, sample_data):
        created = service.create(sample_data)
        fetched = service.get_by_id(created.id)
        assert fetched is not None
        assert fetched.id == created.id

    def test_get_by_id_not_found(self, service):
        assert service.get_by_id("non-existent-id") is None


# ---------------------------------------------------------------------------
# search()
# ---------------------------------------------------------------------------

class TestSearch:
    def test_search_by_name(self, service, sample_data):
        service.create(sample_data)
        results = service.search("Widget")
        assert len(results) == 1

    def test_search_by_description(self, service, sample_data):
        service.create(sample_data)
        results = service.search("testing")
        assert len(results) == 1

    def test_search_case_insensitive(self, service, sample_data):
        service.create(sample_data)
        results = service.search("WIDGET")
        assert len(results) == 1

    def test_search_no_match(self, service, sample_data):
        service.create(sample_data)
        results = service.search("xyz-no-match")
        assert results == []


# ---------------------------------------------------------------------------
# update()
# ---------------------------------------------------------------------------

class TestUpdate:
    def test_update_single_field(self, service, sample_data):
        product = service.create(sample_data)
        updated = service.update(product.id, {"price": 19.99})
        assert updated is not None
        assert updated.price == 19.99
        # Other fields should remain unchanged.
        assert updated.name == "Test Widget"

    def test_update_returns_none_for_missing_product(self, service):
        result = service.update("non-existent", {"name": "x"})
        assert result is None

    def test_update_raises_for_invalid_data(self, service, sample_data):
        product = service.create(sample_data)
        with pytest.raises(ValueError):
            service.update(product.id, {"price": -100})


# ---------------------------------------------------------------------------
# delete()
# ---------------------------------------------------------------------------

class TestDelete:
    def test_delete_existing_product(self, service, sample_data):
        product = service.create(sample_data)
        assert service.delete(product.id) is True
        assert service.get_by_id(product.id) is None

    def test_delete_non_existing_returns_false(self, service):
        assert service.delete("non-existent") is False


# ---------------------------------------------------------------------------
# adjust_stock()
# ---------------------------------------------------------------------------

class TestAdjustStock:
    def test_increase_stock(self, service, sample_data):
        product = service.create(sample_data)
        updated = service.adjust_stock(product.id, 10)
        assert updated.stock == 60  # 50 + 10

    def test_decrease_stock(self, service, sample_data):
        product = service.create(sample_data)
        updated = service.adjust_stock(product.id, -20)
        assert updated.stock == 30  # 50 - 20

    def test_adjust_stock_raises_if_insufficient(self, service, sample_data):
        product = service.create(sample_data)
        with pytest.raises(ValueError, match="Insufficient stock"):
            service.adjust_stock(product.id, -100)  # exceeds available stock

    def test_adjust_stock_returns_none_for_missing_product(self, service):
        result = service.adjust_stock("non-existent", 5)
        assert result is None
