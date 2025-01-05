package mk.finki.ukim.mk.makedonskaberza.repository.impl;

import mk.finki.ukim.mk.makedonskaberza.repository.AnalysisRepository;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;

@Repository
public class AnalysisRepositoryImpl  implements AnalysisRepository {
    @Override
    public List<String> parameters() {
        List<String> params = new ArrayList<>();
        params.add("DMI");
        params.add("CCI");
        params.add("CMO");
        params.add("SO");
        params.add("RSI");
        params.add("SMA");
        params.add("EMA");
        params.add("WMA");
        params.add("SMMA");
        params.add("VWMA");
        return params;
    }

    @Override
    public List<String> intervals() {
        List<String> intervals = new ArrayList<>();
        intervals.add("7");
        intervals.add("14");
        intervals.add("30");
        intervals.add("60");
        intervals.add("120");
        return intervals;
    }
}
