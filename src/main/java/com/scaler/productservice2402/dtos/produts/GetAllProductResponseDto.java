package com.scaler.productservice2402.dtos.produts;

import lombok.Getter;
import lombok.Setter;

import java.util.List;
@Getter
@Setter
public class GetAllProductResponseDto {
    List<GetProductDto> products;
}
