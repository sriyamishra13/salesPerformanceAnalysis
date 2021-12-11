package com.pubsub.gcp.publisher;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.cloud.spring.pubsub.core.PubSubTemplate;
import com.google.cloud.spring.pubsub.integration.outbound.PubSubMessageHandler;

import com.google.cloud.spring.pubsub.support.converter.JacksonPubSubMessageConverter;
import com.google.cloud.spring.pubsub.support.converter.PubSubMessageConverter;
import com.google.protobuf.ByteString;
import com.google.pubsub.v1.PubsubMessage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.PropertySource;
import org.springframework.integration.annotation.MessagingGateway;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.messaging.MessageHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@PropertySource("classpath:application.properties")
public class PublisherSvcApplication {

	public static void main(String[] args) {
		SpringApplication.run(PublisherSvcApplication.class, args);
	}

	private static final String TOPIC = "product-pubsub";

	@Bean
	@ServiceActivator(inputChannel = "pubsubOutputChannel")
	public MessageHandler messageSender(PubSubTemplate pubSubTemplate) {
		return new PubSubMessageHandler(pubSubTemplate, TOPIC);
	}

	@MessagingGateway(defaultRequestChannel = "pubsubOutputChannel")
	public interface PubsubOutboundGateway {
		void sentToPubsub(String text);
	}

	@Bean
	public PubSubMessageConverter pubSubMessageConverter() {
		return new JacksonPubSubMessageConverter(new ObjectMapper());
	}

	@Autowired
	private PubsubOutboundGateway messagingGateway;

	@PostMapping("/publishMessage")
	public String publishMessage() {
		return "Message Published";
	}

	@GetMapping("/api")
	public String healthCheck() {
		return "From App Engine!";
	}

}

	@RestController
	class TestController {
		@GetMapping("/fetch")
		public String healthCheck() {
			return "From App Engine!";
		}
	}
