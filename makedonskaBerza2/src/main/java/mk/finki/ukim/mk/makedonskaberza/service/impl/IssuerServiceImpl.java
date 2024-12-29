package mk.finki.ukim.mk.makedonskaberza.service.impl;

import mk.finki.ukim.mk.makedonskaberza.model.Issuer;
import mk.finki.ukim.mk.makedonskaberza.repository.IssuerRepository;
import mk.finki.ukim.mk.makedonskaberza.service.IssuerService;
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
import java.util.List;

@Service
public class IssuerServiceImpl implements IssuerService {

    private final IssuerRepository repository;
    private final RestTemplate restTemplate;

    public IssuerServiceImpl(IssuerRepository repository, RestTemplate restTemplate) {
        this.repository = repository;
        this.restTemplate = restTemplate;
    }

    @Override
    public List<Issuer> GetAllIssuers() {
        return this.repository.findAll();
    }

    @Override
    public Issuer GetIssuerByCode(String issuercode) {
        return repository.findByIssuercodeIgnoreCase(issuercode);
    }

    @Override
    public List<Issuer> searchResult(String search) {
        return repository.findAllByIssuercodeContainingIgnoreCaseOrIssuernameContainingIgnoreCase(search, search);
    }

    @Override
    public List<Issuer> searchByCode(String code) {
        return repository.findByIssuercodeContainingIgnoreCase(code);
    }

    @Override
    public List<String> getAllIssuerCodes() {
        return this.GetAllIssuers().stream().map(Issuer::getIssuercode).toList();
    }

    @Override
    public List<Issuer> searchCompanies(String name) {
        return repository.findByIssuernameContainingIgnoreCase(name);
    }

    // New getImg Function
    public void getImg(String issuercode) {
        String flaskUrl = "http://localhost:6000/predict";
        String jsonBody = String.format(
                "{\"issuer\": \"%s\"}", issuercode
        );

        // Prepare the HTTP request
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<String> entity = new HttpEntity<>(jsonBody, headers);

        try {
            // Send POST request to Flask's /predict endpoint
            ResponseEntity<Resource> response = restTemplate.exchange(
                    flaskUrl,
                    HttpMethod.POST,
                    entity,
                    Resource.class
            );

            if (response.getStatusCode() == HttpStatus.OK && response.getBody() != null) {
                // Save the image locally
                try (InputStream inputStream = response.getBody().getInputStream()) {
                    Path outputPath = Paths.get("src/main/resources/static/img/stock_prediction_graph.png");
                    Files.createDirectories(outputPath.getParent());
                    Files.copy(inputStream, outputPath, StandardCopyOption.REPLACE_EXISTING);
                } catch (IOException e) {
                    e.printStackTrace();
                    throw new RuntimeException("Error while saving the image", e);
                }
            } else {
                System.out.println("Failed to fetch the image. Status: " + response.getStatusCode());
                throw new RuntimeException("Failed to fetch image from Flask service");
            }
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException("Error during the HTTP request to Flask service", e);
        }
    }
}
