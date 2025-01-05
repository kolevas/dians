package mk.finki.ukim.mk.makedonskaberza.service.impl;


import mk.finki.ukim.mk.makedonskaberza.repository.AnalysisRepository;
import mk.finki.ukim.mk.makedonskaberza.service.AnalysisService;
import mk.finki.ukim.mk.makedonskaberza.service.strategy.context.AnalysisServiceContext;
import org.springframework.stereotype.Service;

import java.io.InputStream;
import java.util.List;

@Service
public class AnalysisServiceImpl implements AnalysisService {

    private final AnalysisServiceContext context;
    private final AnalysisRepository analysisRepository;



    public AnalysisServiceImpl(AnalysisServiceContext context, AnalysisRepository analysisRepository) {
        this.context = context;
        this.analysisRepository = analysisRepository;
    }

    @Override
    public List<String> getParams() {
        return analysisRepository.parameters();
    }

    @Override
    public List<String> getIntervals() {
        return analysisRepository.intervals();
    }

    @Override
    public InputStream getImg(String issuer, String indicator, String interval) {
        return context.getImageGenerationStrategy().generateImage(issuer, indicator,interval);
    }
}