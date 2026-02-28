package com.scaler.productservice2402.dtos.fakestores;

import com.scaler.productservice2402.models.Product;
import lombok.Getter;
import lombok.Setter;
import org.springframework.http.HttpEntity;

@Getter
@Setter
public class FakeStoreCreateProductRequestDto {
    private String title;
    private String description;
    private String category;
    private Double price;
    private String image;
    public static FakeStoreCreateProductRequestDto fromProduct(Product product){
        FakeStoreCreateProductRequestDto fakeStoreCreateProductRequestDto = new FakeStoreCreateProductRequestDto();
        fakeStoreCreateProductRequestDto.setTitle(product.getTitle());
        fakeStoreCreateProductRequestDto.setDescription(product.getDescription());
        fakeStoreCreateProductRequestDto.setCategory(product.getCategoryName());
        fakeStoreCreateProductRequestDto.setPrice(product.getPrice());
        fakeStoreCreateProductRequestDto.setImage(product.getImageUrl());
        return fakeStoreCreateProductRequestDto;
    }
}
