package com.scaler.productservice2402.dtos.produts;

import com.scaler.productservice2402.models.Product;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class GetProductDto {
    private Long id;
    private String title;
    private Double price;
    private String description;
    private String imageUrl;
    public static GetProductDto fromProduct(Product product){
        GetProductDto getProductDto = new GetProductDto();
        getProductDto.setId(product.getId());
        getProductDto.setTitle(product.getTitle());
        getProductDto.setPrice(product.getPrice());
        getProductDto.setDescription(product.getDescription());
        getProductDto.setImageUrl(product.getImageUrl());
        return getProductDto;
    }
}
