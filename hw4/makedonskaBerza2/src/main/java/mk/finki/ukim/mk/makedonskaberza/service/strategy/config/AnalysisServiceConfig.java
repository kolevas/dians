package mk.finki.ukim.mk.makedonskaberza.service.strategy.config;

import mk.finki.ukim.mk.makedonskaberza.service.strategy.impl.FlaskImageGenerationStrategy;
import mk.finki.ukim.mk.makedonskaberza.service.strategy.ImageGenerationStrategy;
import mk.finki.ukim.mk.makedonskaberza.service.strategy.context.AnalysisServiceContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class AnalysisServiceConfig {

    @Bean
    public AnalysisServiceContext analysisServiceContext(RestTemplate restTemplate) {
        // Define strategies for the analysis service
        ImageGenerationStrategy imageGenerationStrategy = new FlaskImageGenerationStrategy(restTemplate);

        // Return the context that manages those strategies
        return new AnalysisServiceContext(imageGenerationStrategy);
    }
}
