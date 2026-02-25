"""
models/product.py
-----------------
Defines the Product data model used throughout the ProductService.

A Product represents a sellable item in the e-commerce catalogue.
It captures core attributes required for display, pricing, and inventory.
"""

from dataclasses import dataclass, field
from typing import Optional
import uuid


@dataclass
class Product:
    """
    Represents a single product in the e-commerce catalogue.

    Attributes:
        id (str): Unique identifier (UUID v4) automatically assigned on creation.
        name (str): Human-readable product name. Must not be empty.
        description (str): Detailed description of the product.
        price (float): Retail price in the store's base currency. Must be >= 0.
        stock (int): Number of units currently available. Must be >= 0.
        category (str): Catalogue category the product belongs to (e.g. "Electronics").
        sku (Optional[str]): Stock-Keeping Unit – an optional external identifier used
            by warehouse systems. Defaults to None when not provided.
    """

    # Mutable default for 'id' requires field(default_factory=...) in dataclasses.
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    price: float = 0.0
    stock: int = 0
    category: str = ""
    sku: Optional[str] = None

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    def validate(self) -> None:
        """
        Validate the product's field values.

        Raises:
            ValueError: If any field contains an invalid value.
        """
        if not self.name or not self.name.strip():
            raise ValueError("Product name must not be empty.")

        if self.price < 0:
            raise ValueError(f"Product price must be >= 0, got {self.price}.")

        if self.stock < 0:
            raise ValueError(f"Product stock must be >= 0, got {self.stock}.")

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Serialise the product to a plain dictionary suitable for JSON responses.

        Returns:
            dict: Key/value representation of the product.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "sku": self.sku,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        """
        Deserialise a product from a plain dictionary (e.g. parsed JSON body).

        Args:
            data (dict): Dictionary containing product fields.

        Returns:
            Product: A new Product instance populated from *data*.

        Note:
            Unknown keys in *data* are silently ignored, which keeps the
            API tolerant of extra fields sent by clients.
        """
        return cls(
            # Preserve the provided 'id' or generate a new one automatically.
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            price=float(data.get("price", 0.0)),
            stock=int(data.get("stock", 0)),
            category=data.get("category", ""),
            sku=data.get("sku"),
        )
