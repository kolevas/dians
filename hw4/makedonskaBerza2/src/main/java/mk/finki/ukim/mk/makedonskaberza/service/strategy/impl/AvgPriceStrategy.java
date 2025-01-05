package mk.finki.ukim.mk.makedonskaberza.service.strategy.impl;

import io.micrometer.observation.Observation;
import mk.finki.ukim.mk.makedonskaberza.repository.HistoryRepository;
import mk.finki.ukim.mk.makedonskaberza.service.strategy.PriceCalculationStrategy;
import mk.finki.ukim.mk.makedonskaberza.model.IssuerHistory;
import java.sql.Date;
import java.time.LocalDateTime;
import java.util.Objects;

public class AvgPriceStrategy implements PriceCalculationStrategy {

    private final HistoryRepository repository;

    public AvgPriceStrategy(HistoryRepository repository) {
        this.repository = repository;
    }

    @Override
    public double calculate(String code, String type){

        Observation.CheckedFunction<IssuerHistory, Double, Throwable> f;
        if(Objects.equals(type, "max"))
            f = IssuerHistory::getMaximumPrice;
        else
            f= IssuerHistory::getMinimumPrice;

        return repository.findIssuerHistoryByIssuerCodeIgnoreCase(code).stream()
                .filter(ih -> {
                    Date entryDate = ih.getEntryDate();
                    if (entryDate == null) {
                        return false;
                    }
                    LocalDateTime ihDate = entryDate.toLocalDate().atStartOfDay();
                    return ihDate.isAfter(LocalDateTime.now().minusYears(1));
                })
                .mapToDouble(i-> {
                    try {
                        return f.apply(i);
                    } catch (Throwable e) {
                        throw new RuntimeException(e);
                    }
                })
                .average()
                .orElse(0);
    }
}



