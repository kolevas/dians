package mk.finki.ukim.mk.makedonskaberza.service.strategy;


import org.springframework.core.io.Resource;

import java.io.InputStream;

public interface ImageProcessingStrategy {
    InputStream processImage(Resource resource, String issuerCode);
}
