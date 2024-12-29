package mk.finki.ukim.mk.makedonskaberza.service.impl;


import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import mk.finki.ukim.mk.makedonskaberza.service.AnalysisService;
import org.springframework.core.io.Resource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.List;

import org.springframework.web.client.RestTemplate;

@Service
public class AnalysisServiceImpl implements AnalysisService {

    private final RestTemplate restTemplate;

    public AnalysisServiceImpl(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @Override
    public List<String> getPrikazi() {
        List<String> prikazi = new ArrayList<>();
        prikazi.add("DMI");
        prikazi.add("CCI");
        prikazi.add("CMO");
        prikazi.add("SO");
        prikazi.add("RSI");
        prikazi.add("SMA");
        prikazi.add("EMA");
        prikazi.add("WMA");
        prikazi.add("SMMA");
        prikazi.add("VWMA");
        return prikazi;
    }

    @Override
    public List<String> getVreminja() {
        List<String> vreminja = new ArrayList<>();
        vreminja.add("7");
        vreminja.add("14");
        vreminja.add("30");
        vreminja.add("60");
        vreminja.add("120");
        return vreminja;
    }

    @Override
    public void getImg(String issuer, String prikaz, String interval) {
        String flaskUrl = "http://localhost:5000/generate";
        String jsonBody = String.format("{\"issuer\": \"%s\", \"interval\": \"%s\", \"prikaz\": \"%s\"}", issuer, interval, prikaz);

        // Prepare the HTTP request
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<String> entity = new HttpEntity<>(jsonBody, headers);

        try {
            // Make the HTTP POST request
            ResponseEntity<Resource> response = restTemplate.exchange(
                    flaskUrl,
                    HttpMethod.POST,
                    entity,
                    Resource.class
            );

            if (response.getStatusCode() == HttpStatus.OK && response.getBody() != null) {
                // Save the image to a file
                try (InputStream inputStream = response.getBody().getInputStream()) {
                    Path outputPath = Paths.get(String.format("src/main/resources/static/img/image_from_flask_%s_%s_%s.png", issuer, prikaz,interval));
                    Files.createDirectories(outputPath.getParent());
                    Files.copy(inputStream, outputPath, StandardCopyOption.REPLACE_EXISTING);
                } catch (IOException e) {
                    // Log the exception
                    e.printStackTrace();
                    throw new RuntimeException("Error while saving the image", e);
                }
            } else {
                // Log the error
                System.out.println("Failed to fetch the image. Status: " + response.getStatusCode());
                throw new RuntimeException("Failed to fetch image from Flask service");
            }
        } catch (Exception e) {
            // Log and handle the error
            e.printStackTrace();
            throw new RuntimeException("Error during the HTTP request to Flask service", e);
        }
    }

}