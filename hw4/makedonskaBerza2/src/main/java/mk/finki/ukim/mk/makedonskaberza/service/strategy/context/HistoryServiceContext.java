package mk.finki.ukim.mk.makedonskaberza.service.strategy.context;

import lombok.Getter;
import mk.finki.ukim.mk.makedonskaberza.service.strategy.PriceCalculationStrategy;
import mk.finki.ukim.mk.makedonskaberza.service.strategy.TransactionCountingStrategy;

@Getter
public class HistoryServiceContext {

    private final PriceCalculationStrategy avgMaxPriceStrategy;
    private final PriceCalculationStrategy avgMinPriceStrategy;
    private final TransactionCountingStrategy transactionsLastYearStrategy;

    public HistoryServiceContext(PriceCalculationStrategy avgMaxPriceStrategy,
                                 PriceCalculationStrategy avgMinPriceStrategy, TransactionCountingStrategy transactionsLastYearStrategy) {
        this.avgMaxPriceStrategy = avgMaxPriceStrategy;
        this.avgMinPriceStrategy = avgMinPriceStrategy;
        this.transactionsLastYearStrategy = transactionsLastYearStrategy;
    }

}


