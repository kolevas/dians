package mk.finki.ukim.mk.makedonskaberza.service.strategy.config;

import mk.finki.ukim.mk.makedonskaberza.repository.HistoryRepository;
import mk.finki.ukim.mk.makedonskaberza.service.strategy.PriceCalculationStrategy;
import mk.finki.ukim.mk.makedonskaberza.service.strategy.TransactionCountingStrategy;
import mk.finki.ukim.mk.makedonskaberza.service.strategy.impl.AvgPriceStrategy;
import mk.finki.ukim.mk.makedonskaberza.service.strategy.context.HistoryServiceContext;
import mk.finki.ukim.mk.makedonskaberza.service.strategy.impl.TransactionsLastYearStrategy;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class HistoryServiceConfig {

    @Bean
    public HistoryServiceContext historyServiceContext(HistoryRepository repository) {
        PriceCalculationStrategy avgMaxPriceStrategy = new AvgPriceStrategy(repository);
        PriceCalculationStrategy avgMinPriceStrategy = new AvgPriceStrategy(repository);
        TransactionCountingStrategy transactionsLastYearStrategy = new TransactionsLastYearStrategy(repository);

        return new HistoryServiceContext(avgMaxPriceStrategy, avgMinPriceStrategy, transactionsLastYearStrategy);
    }
}
