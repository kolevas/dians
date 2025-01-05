package mk.finki.ukim.mk.makedonskaberza.repository;

import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AnalysisRepository {
    List<String> parameters();
    List<String> intervals();
}
