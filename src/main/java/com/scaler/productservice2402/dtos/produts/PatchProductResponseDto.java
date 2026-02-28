package com.scaler.productservice2402.dtos.produts;

import com.scaler.productservice2402.models.Product;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class PatchProductResponseDto {
    private GetProductDto productDto;
}
