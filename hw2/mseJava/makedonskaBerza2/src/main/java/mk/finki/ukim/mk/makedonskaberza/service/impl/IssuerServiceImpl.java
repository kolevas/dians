package mk.finki.ukim.mk.makedonskaberza.service.impl;

import mk.finki.ukim.mk.makedonskaberza.model.Issuer;
import mk.finki.ukim.mk.makedonskaberza.repository.IssuerRepository;
import mk.finki.ukim.mk.makedonskaberza.service.IssuerService;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class IssuerServiceImpl implements IssuerService {
    private final IssuerRepository repository;

    public IssuerServiceImpl(IssuerRepository repository) {
        this.repository = repository;
    }

    @Override
    public List<Issuer> GetAllIssuers() {
        return this.repository.findAll();
    }
}
