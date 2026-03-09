package com.scaler.productservice2402.models;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.List;
@Getter
@Setter
@Entity
public class Category extends BaseModel{
    @Column(unique = true, name = "category_name")
    private String name;
    private String description;
    @OneToMany(fetch = FetchType.EAGER)
    private List<Product> featuredProducts;
    @OneToMany(fetch = FetchType.LAZY, mappedBy = "category", cascade = {CascadeType.PERSIST, CascadeType.MERGE, CascadeType.REMOVE})
    private List<Product> allProducts;
}
