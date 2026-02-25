package com.scaler.productservice2402.services;

import com.scaler.productservice2402.dtos.FakeStoreCreateProductRequestDto;
import com.scaler.productservice2402.dtos.FakeStoreCreateProductResponseDto;
import com.scaler.productservice2402.models.Product;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

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
        FakeStoreCreateProductResponseDto responseDto = restTemplate
                .postForObject("https://fakestoreapi.com/products/",
                        fakeStoreCreateProductRequestDto,
                        FakeStoreCreateProductResponseDto.class);
        Product productResponse = new Product();
        productResponse.setId(responseDto.getId());
        productResponse.setTitle(responseDto.getTitle());
        productResponse.setCategoryName(responseDto.getCategory());
        productResponse.setDescription(responseDto.getDescription());
        productResponse.setPrice(responseDto.getPrice());
        productResponse.setImageUrl(responseDto.getImage());
        return productResponse;
    }
}
