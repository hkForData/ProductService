package com.scaler.productservice2402.dtos;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class FakeStoreCreateProductResponseDto {
    private Long id;
    private String title;
    private String description;
    private String category;
    private Double price;
    private String image;
}
