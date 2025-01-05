package mk.finki.ukim.mk.makedonskaberza.service.strategy.impl;

import mk.finki.ukim.mk.makedonskaberza.service.strategy.ImageProcessingStrategy;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Component;


import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;

@Component
public class LocalImageSaveStrategy implements ImageProcessingStrategy {
    @Override
    public InputStream processImage(Resource resource, String issuerCode) {
        try (InputStream inputStream = resource.getInputStream()) {
            return inputStream;
        } catch (IOException e) {
            throw new RuntimeException("Error while sending the image locally", e);
        }
    }
}
