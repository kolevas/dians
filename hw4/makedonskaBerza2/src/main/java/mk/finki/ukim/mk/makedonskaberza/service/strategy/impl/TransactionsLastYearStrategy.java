package mk.finki.ukim.mk.makedonskaberza.service.strategy.impl;

import mk.finki.ukim.mk.makedonskaberza.repository.HistoryRepository;
import mk.finki.ukim.mk.makedonskaberza.service.strategy.TransactionCountingStrategy;

import java.sql.Date;
import java.time.LocalDateTime;

public class TransactionsLastYearStrategy implements TransactionCountingStrategy {
    private final HistoryRepository repository;

    public TransactionsLastYearStrategy(HistoryRepository repository) {
        this.repository = repository;
    }

    @Override
    public long countTransactions(String code) {
        return repository.findIssuerHistoryByIssuerCodeIgnoreCase(code).stream()
                .filter(ih -> {
                    Date entryDate = ih.getEntryDate();
                    if (entryDate == null) {
                        return false;
                    }
                    LocalDateTime ihDate = entryDate.toLocalDate().atStartOfDay();
                    return ihDate.isAfter(LocalDateTime.now().minusYears(1));
                })
                .count();
    }
}

