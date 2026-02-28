package com.scaler.productservice2402.controllers;

import com.scaler.productservice2402.dtos.ErrorResponseDto;
import com.scaler.productservice2402.dtos.produts.*;
import com.scaler.productservice2402.models.Product;
import com.scaler.productservice2402.services.ProductService;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/products")
public class ProductController {
    ProductService productService;
    public ProductController(@Qualifier("fakeStoreProductService") ProductService productService) {
        this.productService = productService;
    }
    @PostMapping("")
    public CreateProductResponseDto createProduct(@RequestBody CreateProductRequestDto createProductRequestDto){
        Product product = productService.createProduct(createProductRequestDto.toProduct());
        return CreateProductResponseDto.fromProduct(product);
    }

    @GetMapping("")
    public GetAllProductResponseDto getAllProduct(){
        List<Product> products = productService.getAllProducts();
        List<GetProductDto> responseDtos = new ArrayList<>();
        GetAllProductResponseDto response = new GetAllProductResponseDto();

        for(Product product: products){
            responseDtos.add(GetProductDto.fromProduct(product));
        }
        response.setProducts(responseDtos);
        return response;
    }

    @GetMapping("/{id}")
    public CreateProductResponseDto getSingleProduct(@PathVariable("id") Long id)
    {
        Product product = productService.getSingleProduct(id);
        return CreateProductResponseDto.fromProduct(product);
    }

    @DeleteMapping("/{id}")
    public void deleteProduct(@PathVariable("id") Long id)
    {
        productService.deleteProduct(id);
    }
    @PatchMapping("/{id}")
    public PatchProductResponseDto updateProduct(@PathVariable("id") Long id, @RequestBody CreateProductDto createProductDto)
    {
        //patch
        Product product = productService.partialUpdateProduct(id, createProductDto.toProduct());
        PatchProductResponseDto response = new PatchProductResponseDto();
        response.setProductDto(GetProductDto.fromProduct(product));
        return response;
    }
    public void replaceProduct(){
        //put
    }

}
