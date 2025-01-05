package mk.finki.ukim.mk.makedonskaberza.service;

import java.io.InputStream;
import java.util.List;

public interface AnalysisService {

    List<String> getParams();

    List<String> getIntervals();

    InputStream getImg(String issuer, String indicator, String interval);
}
