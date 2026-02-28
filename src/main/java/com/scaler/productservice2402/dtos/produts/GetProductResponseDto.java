package com.scaler.productservice2402.dtos;

import com.scaler.productservice2402.models.Product;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class GetProductResponseDto {
    private Long id;
    private String title;
    private Double price;
    private String description;
    private String imageUrl;
    public static GetProductResponseDto fromProduct(Product product){
        GetProductResponseDto getProductResponseDto = new GetProductResponseDto();
        getProductResponseDto.setId(product.getId());
        getProductResponseDto.setTitle(product.getTitle());
        getProductResponseDto.setPrice(product.getPrice());
        getProductResponseDto.setDescription(product.getDescription());
        getProductResponseDto.setImageUrl(product.getImageUrl());
        return getProductResponseDto;
    }
}
