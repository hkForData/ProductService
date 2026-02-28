package com.scaler.productservice2402.services;

import com.scaler.productservice2402.models.Product;

import java.util.List;

public interface ProductService {
    Product createProduct(Product product);
    Product getSingleProduct(Long id);

    void deleteProduct(Long id);
    List<Product> getAllProducts();
     Product partialUpdateProduct(Long productId, Product product);
     void replaceProduct(Long id, Product product);
}
