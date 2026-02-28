package com.scaler.productservice2402.services;

import com.scaler.productservice2402.dtos.fakestores.FakeStoreCreateProductRequestDto;
import com.scaler.productservice2402.dtos.fakestores.FakeStoreGetProductResponseDto;
import com.scaler.productservice2402.exceptions.ProductNotFoundException;
import com.scaler.productservice2402.models.Product;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.List;

@Service("fakeStoreProductService")
public class ProductServiceFakeStoreImpl implements ProductService{

    private RestTemplate restTemplate;
    ProductServiceFakeStoreImpl(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }
    @Override
    public Product createProduct(Product product) {
        FakeStoreCreateProductRequestDto fakeStoreCreateProductRequestDto = new FakeStoreCreateProductRequestDto();
        fakeStoreCreateProductRequestDto.setCategory(product.getCategoryName());
        fakeStoreCreateProductRequestDto.setDescription(product.getDescription());
        fakeStoreCreateProductRequestDto.setPrice(product.getPrice());
        fakeStoreCreateProductRequestDto.setImage(product.getImageUrl());
        fakeStoreCreateProductRequestDto.setTitle(product.getTitle());
        FakeStoreGetProductResponseDto responseDto = restTemplate
                .postForObject("https://fakestoreapi.com/products/",
                        fakeStoreCreateProductRequestDto,
                        FakeStoreGetProductResponseDto.class);
        return responseDto.toProduct();
    }

    @Override
    public Product getSingleProduct(Long id){
        FakeStoreGetProductResponseDto responseDto = restTemplate.getForObject("https://fakestoreapi.com/products/{id}", FakeStoreGetProductResponseDto.class, id);
        if(responseDto == null){
            throw new ProductNotFoundException("Product with id " + id + " not found");
        }
        Product productResponse = new Product();
        productResponse.setId(responseDto.getId());
        productResponse.setTitle(responseDto.getTitle());
        productResponse.setCategoryName(responseDto.getCategory());
        productResponse.setDescription(responseDto.getDescription());
        productResponse.setPrice(responseDto.getPrice());
        productResponse.setImageUrl(responseDto.getImage());
        return productResponse;
    }

    @Override
    public void deleteProduct(Long id) {
        restTemplate.delete("https://fakestoreapi.com/products/{id}", id);
    }

    @Override
    public List<Product> getAllProducts() {
        FakeStoreGetProductResponseDto[] fakeStoreGetProductResponseDtos = restTemplate.getForObject("https://fakestoreapi.com/products/", FakeStoreGetProductResponseDto[].class);
       List<Product> products = new ArrayList<>();
       for(FakeStoreGetProductResponseDto fakeStoreGetProductResponseDto : fakeStoreGetProductResponseDtos){
           products.add(fakeStoreGetProductResponseDto.toProduct());
       }
       return products;
    }

    @Override
    public Product partialUpdateProduct(Long productId, Product product) {
        HttpEntity<FakeStoreCreateProductRequestDto> requestEntity = new HttpEntity<>(FakeStoreCreateProductRequestDto.fromProduct(product));
        ResponseEntity<FakeStoreGetProductResponseDto> responseEntity= restTemplate.exchange("https://fakestoreapi.com/products/{id}",
                HttpMethod.PATCH, requestEntity, FakeStoreGetProductResponseDto.class);
        return responseEntity.getBody().toProduct();
    }


    @Override
    public void replaceProduct(Long id, Product product) {

    }
}
