package mk.finki.ukim.mk.makedonskaberza.service.impl;

import mk.finki.ukim.mk.makedonskaberza.model.IssuerHistory;
import mk.finki.ukim.mk.makedonskaberza.repository.HistoryRepository;
import mk.finki.ukim.mk.makedonskaberza.service.HistoryService;
import org.springframework.stereotype.Service;

import java.sql.Date;
import java.util.ArrayList;
import java.util.List;

@Service
public class HistoryServiceImpl implements HistoryService {
    private final HistoryRepository repository;

    public HistoryServiceImpl(HistoryRepository repository) {
        this.repository = repository;
    }


    @Override
    public List<IssuerHistory> GetHistoryForCompany(String issuerCode) {
        return this.repository.findByIssuerCodeOrderByEntryDateDesc(issuerCode);
    }

    @Override
    public List<IssuerHistory> GetHistoryForCompany(String issuerCode, Date startDate, Date endDate) {
        return this.repository.findByIssuerCodeAndEntryDateBetweenOrderByEntryDateDesc(issuerCode, startDate, endDate);
    }
}
