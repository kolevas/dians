package mk.finki.ukim.mk.makedonskaberza.service.impl;

import mk.finki.ukim.mk.makedonskaberza.model.Issuer;
import mk.finki.ukim.mk.makedonskaberza.repository.IssuerRepository;
import mk.finki.ukim.mk.makedonskaberza.service.IssuerService;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class IssuerServiceImpl implements IssuerService {
    private final IssuerRepository repository;

    public IssuerServiceImpl(IssuerRepository repository) {
        this.repository = repository;
    }

    @Override
    public List<Issuer> GetAllIssuers() { return this.repository.findAll();    }


    @Override
    public Issuer GetIssuerByCode(String issuercode) {return repository.findByIssuercodeIgnoreCase(issuercode);}

    @Override
    public List<Issuer> searchResult(String search) {
        return repository.findAllByIssuercodeContainingIgnoreCaseOrIssuernameContainingIgnoreCase(search,search);
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

}
