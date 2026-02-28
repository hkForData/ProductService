package com.scaler.productservice2402.dtos;

import com.scaler.productservice2402.models.Product;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class CreateProductDto {
    private Long id;
    private String title;
    private Double price;
    private String description;
    private String imageUrl;
    public static  CreateProductDto fromProduct(Product product){
        CreateProductDto createProductDto = new CreateProductDto();
        createProductDto.setId(product.getId());
        createProductDto.setTitle(product.getTitle());
        createProductDto.setPrice(product.getPrice());
        createProductDto.setDescription(product.getDescription());
        createProductDto.setImageUrl(product.getImageUrl());
        return createProductDto;
    }
}
