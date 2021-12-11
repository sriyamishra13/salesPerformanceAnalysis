package com.pubsub.gcp.publisher;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.DataInput;
import java.io.IOException;

@Service
@AllArgsConstructor
public class ProductService {

    @Autowired
    public ProductRepository productRepository;

    public void persistProductDetails(ProductData productData) {
        Product product = new Product();
        product.setCategory(productData.getCATEGORY());
        product.setConsole(productData.getCONSOLE());
        product.setPublisher(productData.getPUBLISHER());
        product.setCriticsPoints(productData.getCRITICS_POINTS());
        product.setRating(productData.getRATING());
        product.setUserPoints(productData.getUSER_POINTS());
        product.setYear(productData.getYEAR());

        productRepository.save(product);
    }

}
