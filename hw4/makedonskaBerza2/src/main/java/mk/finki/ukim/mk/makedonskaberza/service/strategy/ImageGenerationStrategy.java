package mk.finki.ukim.mk.makedonskaberza.service.strategy;

import java.io.InputStream;

public interface ImageGenerationStrategy {
    InputStream generateImage(String issuer, String indicator, String interval);
}