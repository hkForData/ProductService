package com.scaler.productservice2402.controllers;

import com.scaler.productservice2402.dtos.CreateProductRequestDto;
import com.scaler.productservice2402.dtos.CreateProductResponseDto;
import com.scaler.productservice2402.models.Product;
import com.scaler.productservice2402.services.ProductService;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/products")
public class ProductController {
    ProductService productService;
    public ProductController(@Qualifier("fakeStoreProductService") ProductService productService) {
        this.productService = productService;
    }
    @PostMapping("")
    public CreateProductResponseDto createProduct(@RequestBody CreateProductRequestDto createProductRequestDto){
        createProductRequestDto.getPrice();
        Product product = productService.createProduct(createProductRequestDto.toProduct());
        return CreateProductResponseDto.fromProduct(product);
    }

    @GetMapping("")
    public void getProduct(){

    }

    @GetMapping("/{id}")
    public String getSingleProduct(@PathVariable("id") Long id)
    {
        return "Here is product " +id;
    }

    @DeleteMapping("/{id}")
    public void deleteProduct(@PathVariable("id") Long id)
    {

    }
    public void updateProduct(){
        //patch
    }
    public void replaceProduct(){
        //put
    }
}
