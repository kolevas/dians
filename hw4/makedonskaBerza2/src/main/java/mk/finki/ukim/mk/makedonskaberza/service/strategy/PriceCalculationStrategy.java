package mk.finki.ukim.mk.makedonskaberza.service.strategy;

public interface PriceCalculationStrategy {
    double calculate(String issuerCode, String type);
}
