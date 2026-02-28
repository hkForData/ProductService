package com.scaler.productservice2402.dtos.fakestores;

import com.scaler.productservice2402.models.Product;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class FakeStoreGetProductResponseDto {
    private Long id;
    private String title;
    private String description;
    private String category;
    private Double price;
    private String image;
    public Product toProduct(){
        Product product = new Product();
        product.setId(this.getId());
        product.setTitle(this.getTitle());
        product.setDescription(this.getDescription());
        product.setCategoryName(this.getCategory());
        product.setPrice(this.getPrice());
        product.setImageUrl(this.getImage());
        return product;
    }
}
