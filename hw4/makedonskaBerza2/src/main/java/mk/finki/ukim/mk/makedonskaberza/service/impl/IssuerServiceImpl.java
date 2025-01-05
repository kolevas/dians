package mk.finki.ukim.mk.makedonskaberza.service.impl;

import mk.finki.ukim.mk.makedonskaberza.model.Issuer;
import mk.finki.ukim.mk.makedonskaberza.repository.IssuerRepository;
import mk.finki.ukim.mk.makedonskaberza.service.IssuerService;
import mk.finki.ukim.mk.makedonskaberza.service.strategy.context.IssuerServiceContext;
import org.springframework.core.io.Resource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.io.InputStream;
import java.util.List;

@Service
public class IssuerServiceImpl implements IssuerService {

    private final IssuerRepository repository;
    private final RestTemplate restTemplate;
    private final IssuerServiceContext context;

    public IssuerServiceImpl(IssuerRepository repository, RestTemplate restTemplate, IssuerServiceContext context) {
        this.repository = repository;
        this.restTemplate = restTemplate;
        this.context = context;
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


    @Override
    public InputStream pricePredictionImage(String issuerCode) {
        String flaskUrl = "http://localhost:6000/predict";
        String jsonBody = String.format("{\"issuer\": \"%s\"}", issuerCode);

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
                return context.getImageProcessingStrategy().processImage(response.getBody(), issuerCode);
            } else {
                throw new RuntimeException("Failed to fetch image from Flask service. Status: " + response.getStatusCode());
            }
        } catch (Exception e) {
            throw new RuntimeException("Error during the HTTP request to Flask service", e);
        }
    }
}
