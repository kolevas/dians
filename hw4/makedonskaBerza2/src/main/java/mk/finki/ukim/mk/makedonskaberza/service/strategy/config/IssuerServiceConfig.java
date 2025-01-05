package mk.finki.ukim.mk.makedonskaberza.service.strategy.config;

import mk.finki.ukim.mk.makedonskaberza.service.strategy.context.IssuerServiceContext;
import mk.finki.ukim.mk.makedonskaberza.service.strategy.impl.LocalImageSaveStrategy;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class IssuerServiceConfig {

    @Bean
    public IssuerServiceContext imageProcessingServiceContext(LocalImageSaveStrategy localImageSaveStrategy) {
        return new IssuerServiceContext(localImageSaveStrategy);
    }
}
