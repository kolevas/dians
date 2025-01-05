package mk.finki.ukim.mk.makedonskaberza.service.strategy.context;

import lombok.Getter;
import mk.finki.ukim.mk.makedonskaberza.service.strategy.ImageProcessingStrategy;

@Getter
public class IssuerServiceContext {
    private final ImageProcessingStrategy imageProcessingStrategy;

    public IssuerServiceContext(ImageProcessingStrategy imageProcessingStrategy) {
        this.imageProcessingStrategy = imageProcessingStrategy;
    }
}
