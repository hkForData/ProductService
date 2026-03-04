package com.scaler.productservice2402.repositories;

import com.scaler.productservice2402.models.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    //update is also done by save method only, if id is present then
    // JPA will update otherwise it will create new record
    Product save(Product product);
}
