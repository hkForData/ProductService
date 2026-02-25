"""
routes/product_routes.py
------------------------
Flask Blueprint that exposes the ProductService over HTTP.

Endpoint summary
----------------
GET    /api/products              – List all products (supports ?category= and ?q= filters)
POST   /api/products              – Create a new product
GET    /api/products/<id>         – Retrieve a single product by ID
PUT    /api/products/<id>         – Update an existing product
DELETE /api/products/<id>         – Delete a product
PATCH  /api/products/<id>/stock   – Adjust stock level
"""

from flask import Blueprint, jsonify, request
from services.product_service import ProductService

# A Blueprint groups related routes so they can be registered on the app with
# a common URL prefix (see app.py: url_prefix="/api/products").
product_bp = Blueprint("products", __name__)

# Module-level service instance.
# In a larger application you would use dependency injection or an
# application factory pattern instead of a module-level singleton.
_service = ProductService()


# ---------------------------------------------------------------------------
# List / Search
# ---------------------------------------------------------------------------

@product_bp.route("/", methods=["GET"])
def list_products():
    """
    GET /api/products/

    Returns a JSON array of all products.

    Query parameters:
        category (str, optional): Filter by product category.
        q        (str, optional): Full-text search across name and description.

    Response 200:
        [{"id": "...", "name": "...", ...}, ...]
    """
    category = request.args.get("category")
    query = request.args.get("q")

    if query:
        # Search takes precedence over category filter when both are provided.
        products = _service.search(query)
    else:
        products = _service.get_all(category=category)

    # Serialise every Product to a plain dict before handing to jsonify.
    return jsonify([p.to_dict() for p in products]), 200


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------

@product_bp.route("/", methods=["POST"])
def create_product():
    """
    POST /api/products/

    Create a new product from the JSON request body.

    Request body (JSON):
        {
            "name":        "Widget Pro",          # required
            "description": "A great widget",
            "price":       9.99,
            "stock":       100,
            "category":    "Widgets",
            "sku":         "WGT-PRO-001"          # optional
        }

    Response 201 – created product as JSON.
    Response 400 – validation error message.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    try:
        product = _service.create(data)
    except ValueError as exc:
        # Return the validation message to the caller so they can fix their input.
        return jsonify({"error": str(exc)}), 400

    return jsonify(product.to_dict()), 201


# ---------------------------------------------------------------------------
# Read single
# ---------------------------------------------------------------------------

@product_bp.route("/<string:product_id>", methods=["GET"])
def get_product(product_id: str):
    """
    GET /api/products/<product_id>

    Retrieve a single product by its UUID.

    Response 200 – product as JSON.
    Response 404 – product not found.
    """
    product = _service.get_by_id(product_id)
    if product is None:
        return jsonify({"error": f"Product '{product_id}' not found."}), 404

    return jsonify(product.to_dict()), 200


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------

@product_bp.route("/<string:product_id>", methods=["PUT"])
def update_product(product_id: str):
    """
    PUT /api/products/<product_id>

    Update fields of an existing product.  Supports partial updates – only
    the fields present in the request body are modified.

    Request body (JSON):
        Any subset of the product fields (name, description, price, stock,
        category, sku).

    Response 200 – updated product as JSON.
    Response 400 – validation error.
    Response 404 – product not found.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    try:
        product = _service.update(product_id, data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if product is None:
        return jsonify({"error": f"Product '{product_id}' not found."}), 404

    return jsonify(product.to_dict()), 200


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------

@product_bp.route("/<string:product_id>", methods=["DELETE"])
def delete_product(product_id: str):
    """
    DELETE /api/products/<product_id>

    Delete a product by its UUID.

    Response 204 – deleted successfully (no body).
    Response 404 – product not found.
    """
    deleted = _service.delete(product_id)
    if not deleted:
        return jsonify({"error": f"Product '{product_id}' not found."}), 404

    # 204 No Content – the resource no longer exists.
    return "", 204


# ---------------------------------------------------------------------------
# Stock adjustment
# ---------------------------------------------------------------------------

@product_bp.route("/<string:product_id>/stock", methods=["PATCH"])
def adjust_stock(product_id: str):
    """
    PATCH /api/products/<product_id>/stock

    Adjust a product's stock level by a given quantity.

    Request body (JSON):
        {"quantity": <int>}   # positive to add, negative to remove

    Response 200 – updated product as JSON.
    Response 400 – missing/invalid quantity, or insufficient stock.
    Response 404 – product not found.
    """
    data = request.get_json(silent=True)
    if not data or "quantity" not in data:
        return jsonify({"error": "'quantity' field is required."}), 400

    try:
        quantity = int(data["quantity"])
    except (TypeError, ValueError):
        return jsonify({"error": "'quantity' must be an integer."}), 400

    try:
        product = _service.adjust_stock(product_id, quantity)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if product is None:
        return jsonify({"error": f"Product '{product_id}' not found."}), 404

    return jsonify(product.to_dict()), 200
