package mk.finki.ukim.mk.makedonskaberza.service.strategy.impl;

import mk.finki.ukim.mk.makedonskaberza.service.strategy.ImageGenerationStrategy;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;
import java.io.InputStream;


@Service
public class FlaskImageGenerationStrategy implements ImageGenerationStrategy {

    private final RestTemplate restTemplate;

    @Value("${techanalysis.baseurl}")
    private String baseURL;

    public FlaskImageGenerationStrategy(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @Override
    public InputStream generateImage(String issuer, String indicator, String interval) {

        String flaskUrl = baseURL + "/generate";
        String jsonBody = String.format("{\"issuer\": \"%s\", \"interval\": \"%s\", \"prikaz\": \"%s\"}", issuer, interval, indicator);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<String> entity = new HttpEntity<>(jsonBody, headers);

        try {
            ResponseEntity<Resource> response = restTemplate.exchange(
                    flaskUrl,
                    HttpMethod.POST,
                    entity,
                    Resource.class
            );

            if (response.getStatusCode() == HttpStatus.OK && response.getBody() != null) {

                try (InputStream inputStream = response.getBody().getInputStream()) {
                    return inputStream;
                } catch (IOException e) {
                    throw new RuntimeException("Error while sending the image", e);
                }
            } else {
                System.out.println("Failed to fetch the image. Status: " + response.getStatusCode());
                throw new RuntimeException("Failed to fetch image from Flask service");
            }
        } catch (Exception e) {
            throw new RuntimeException("Error during the HTTP request to Flask service", e);
        }
    }
}
