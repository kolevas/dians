package mk.finki.ukim.mk.makedonskaberza.service;

import java.util.List;

public interface AnalysisService {
//    List<String> getNames();

    List<String> getPrikazi();

    List<String> getVreminja();

    void getImg(String issuer, String prikaz, String interval);
}
