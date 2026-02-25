"""
ProductService - E-commerce Product Microservice
=================================================
This module defines the main Flask application for the ProductService,
an e-commerce microservice responsible for managing products.

Responsibilities:
- CRUD operations on products (Create, Read, Update, Delete)
- Product search and filtering
- Inventory/stock management

Usage:
    python app.py
"""

from flask import Flask
from routes.product_routes import product_bp

# Initialize the Flask application
app = Flask(__name__)

# Register the product blueprint, which groups all product-related endpoints
# under the "/api/products" URL prefix.
app.register_blueprint(product_bp, url_prefix="/api/products")


if __name__ == "__main__":
    # Run the development server on port 5000 with debug mode enabled.
    # In production, use a WSGI server (e.g., gunicorn) instead.
    app.run(debug=True, port=5000)
