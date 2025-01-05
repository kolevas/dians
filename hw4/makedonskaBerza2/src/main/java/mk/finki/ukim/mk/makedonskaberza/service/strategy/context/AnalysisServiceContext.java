package mk.finki.ukim.mk.makedonskaberza.service.strategy.context;

import lombok.Getter;
import mk.finki.ukim.mk.makedonskaberza.service.strategy.ImageGenerationStrategy;

@Getter
public class AnalysisServiceContext {
    private final ImageGenerationStrategy imageGenerationStrategy;

    public AnalysisServiceContext(ImageGenerationStrategy imageGenerationStrategy) {
        this.imageGenerationStrategy = imageGenerationStrategy;
    }

}
