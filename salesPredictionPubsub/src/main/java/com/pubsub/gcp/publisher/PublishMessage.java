package com.pubsub.gcp.publisher;

import com.google.cloud.spring.pubsub.core.publisher.PubSubPublisherTemplate;

import jdk.jfr.internal.Logger;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.concurrent.ExecutionException;

@RestController
public class PublishMessage {

    private final static Log LOGGER = LogFactory.getLog(PublishMessage.class);

    @Autowired
    private final PubSubPublisherTemplate pubSubPublisherTemplate;

    @Autowired
    public ProductService productService;

    PublishMessage(PubSubPublisherTemplate pubSubPublisherTemplate) {
       this.pubSubPublisherTemplate = pubSubPublisherTemplate;
    }

    @PostMapping("/product_details")
    void pushProductDetails(@RequestBody ProductData message) throws ExecutionException, InterruptedException {
        LOGGER.info("Message received = " + message);
        String messageId = pubSubPublisherTemplate.publish("product-pubsub", message).get();
        LOGGER.info("Message published with ID: " + messageId);
        productService.persistProductDetails(message);
    }

}
