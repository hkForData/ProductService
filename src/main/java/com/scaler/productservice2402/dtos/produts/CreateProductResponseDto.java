package com.scaler.productservice2402.dtos.produts;

import com.scaler.productservice2402.models.Product;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class CreateProductResponseDto {
    private Long id;
    private String title;
    private Double price;
    private String description;
    private String imageUrl;

    public static CreateProductResponseDto fromProduct(Product product){
        CreateProductResponseDto createProductResponseDto = new CreateProductResponseDto();
        createProductResponseDto.setId(product.getId());
        createProductResponseDto.setTitle(product.getTitle());
        createProductResponseDto.setPrice(product.getPrice());
        createProductResponseDto.setDescription(product.getDescription());
        createProductResponseDto.setImageUrl(product.getImageUrl());
        return createProductResponseDto;
    }
}
