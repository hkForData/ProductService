package com.scaler.productservice2402.services;

import com.scaler.productservice2402.exceptions.ProductNotFoundException;
import com.scaler.productservice2402.models.Category;
import com.scaler.productservice2402.models.Product;
import com.scaler.productservice2402.repositories.CategoryRepository;
import com.scaler.productservice2402.repositories.ProductRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

import static org.springframework.data.jpa.domain.AbstractPersistable_.id;

@Service("dbProductService")
public class ProductServiceDBImpl implements ProductService{

    private ProductRepository productRepository;
    private CategoryRepository categoryRepository;
    ProductServiceDBImpl(ProductRepository productRepository, CategoryRepository categoryRepository){
        this.productRepository = productRepository;
        this.categoryRepository = categoryRepository;
    }
    @Override
    public Product createProduct(Product product) {
        Category category = getCategoryToBeInProduct(product);
        product.setCategory(category);
        Product savedProduct = productRepository.save(product);
        return savedProduct;
    }

    @Override
    public Product getSingleProduct(Long id) {
        return null;
    }

    @Override
    public void deleteProduct(Long id) {

    }

    @Override
    public List<Product> getAllProducts() {
        return productRepository.findAll();
    }

    @Override
    public Product partialUpdateProduct(Long productId, Product product) {
        Optional<Product> productToUpdate = productRepository.findById(productId);
        if(productToUpdate.isEmpty()){
            throw new ProductNotFoundException("Product with id " + productId + " not found");
        }
        Product existingProduct = getExistingProduct(product, productToUpdate);
        Category category = getCategoryToBeInProduct(product);
        existingProduct.setCategory(category);
        return productRepository.save(existingProduct);
    }

    private static Product getExistingProduct(Product product, Optional<Product> productToUpdate) {
        Product existingProduct = productToUpdate.get();
        if(product.getDescription() != null){
            existingProduct.setDescription(product.getDescription());
        }
        if(product.getPrice() != null){
            existingProduct.setPrice(product.getPrice());
        }
        if(product.getTitle() != null){
            existingProduct.setTitle(product.getTitle());
        }
        if(product.getImageUrl() != null){
            existingProduct.setImageUrl(product.getImageUrl());
        }
        return existingProduct;
    }

    private Category getCategoryToBeInProduct(Product product) {
        String categoryName = product.getCategory().getName();
        Optional<Category> category = categoryRepository.findByName(categoryName);
        Category categoryToBeInProduct;
        if(category.isEmpty()){
            Category toSaveCategory = new Category();
            toSaveCategory.setName(categoryName);
            categoryToBeInProduct = toSaveCategory;
        }
        else {
            categoryToBeInProduct = category.get();
        }
        return categoryToBeInProduct;
    }

    @Override
    public void replaceProduct(Long id, Product product) {

    }
}
