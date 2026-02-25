"""
services/product_service.py
----------------------------
Business-logic layer for product management.

This service acts as the single source of truth for product operations.
It sits between the HTTP route handlers (routes/product_routes.py) and the
data store.  Using this layer keeps the route handlers thin and makes the
business logic easy to unit-test independently of HTTP concerns.

In this implementation an in-memory dictionary is used as the backing store
to keep the project self-contained.  Replacing it with a real database (e.g.
PostgreSQL via SQLAlchemy) requires changes only in this file.
"""

from typing import Dict, List, Optional
from models.product import Product


class ProductService:
    """
    Service class that encapsulates all product-related business logic.

    The in-memory store (``_products``) maps product id → Product instance.
    """

    def __init__(self) -> None:
        # In-memory store: {product_id: Product}
        # In a production environment this would be replaced by a database
        # session or repository object injected via the constructor.
        self._products: Dict[str, Product] = {}

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def get_all(self, category: Optional[str] = None) -> List[Product]:
        """
        Return all products, optionally filtered by category.

        Args:
            category (Optional[str]): When provided, only products whose
                ``category`` attribute matches (case-insensitive) are returned.

        Returns:
            List[Product]: List of matching Product objects.
        """
        products = list(self._products.values())

        if category:
            # Normalise to lower-case for case-insensitive comparison.
            products = [p for p in products if p.category.lower() == category.lower()]

        return products

    def get_by_id(self, product_id: str) -> Optional[Product]:
        """
        Retrieve a single product by its unique identifier.

        Args:
            product_id (str): UUID of the product to fetch.

        Returns:
            Optional[Product]: The matching Product, or ``None`` if not found.
        """
        return self._products.get(product_id)

    def search(self, query: str) -> List[Product]:
        """
        Search products whose name or description contains *query*.

        The search is case-insensitive and uses simple substring matching.
        For large catalogues this should be replaced with a full-text search
        solution (e.g. Elasticsearch).

        Args:
            query (str): The search term.

        Returns:
            List[Product]: Products that match the query.
        """
        query_lower = query.lower()
        return [
            p
            for p in self._products.values()
            if query_lower in p.name.lower() or query_lower in p.description.lower()
        ]

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def create(self, data: dict) -> Product:
        """
        Create and persist a new product.

        Args:
            data (dict): Raw product data (typically from a JSON request body).

        Returns:
            Product: The newly created product.

        Raises:
            ValueError: If the product data fails validation (see Product.validate).
        """
        product = Product.from_dict(data)
        # Validate before persisting to catch bad data early.
        product.validate()
        self._products[product.id] = product
        return product

    def update(self, product_id: str, data: dict) -> Optional[Product]:
        """
        Update an existing product's fields.

        Only fields present in *data* are updated; omitted fields keep their
        current values (partial/PATCH-style semantics).

        Args:
            product_id (str): UUID of the product to update.
            data (dict): Fields to update.

        Returns:
            Optional[Product]: The updated product, or ``None`` if not found.

        Raises:
            ValueError: If the updated product fails validation.
        """
        product = self._products.get(product_id)
        if product is None:
            return None

        # Apply only the provided fields to support partial updates.
        if "name" in data:
            product.name = data["name"]
        if "description" in data:
            product.description = data["description"]
        if "price" in data:
            product.price = float(data["price"])
        if "stock" in data:
            product.stock = int(data["stock"])
        if "category" in data:
            product.category = data["category"]
        if "sku" in data:
            product.sku = data["sku"]

        # Re-validate after applying changes.
        product.validate()
        return product

    def delete(self, product_id: str) -> bool:
        """
        Delete a product by its unique identifier.

        Args:
            product_id (str): UUID of the product to delete.

        Returns:
            bool: ``True`` if the product was found and deleted, ``False`` otherwise.
        """
        if product_id in self._products:
            del self._products[product_id]
            return True
        return False

    def adjust_stock(self, product_id: str, quantity: int) -> Optional[Product]:
        """
        Adjust a product's stock level by *quantity* units.

        Positive values increase stock (e.g. restocking); negative values
        decrease it (e.g. after a sale).

        Args:
            product_id (str): UUID of the product.
            quantity (int): Number of units to add (positive) or remove (negative).

        Returns:
            Optional[Product]: The updated product, or ``None`` if not found.

        Raises:
            ValueError: If the adjustment would make the stock level negative.
        """
        product = self._products.get(product_id)
        if product is None:
            return None

        new_stock = product.stock + quantity
        if new_stock < 0:
            raise ValueError(
                f"Insufficient stock. Current stock: {product.stock}, "
                f"requested adjustment: {quantity}."
            )

        product.stock = new_stock
        return product
