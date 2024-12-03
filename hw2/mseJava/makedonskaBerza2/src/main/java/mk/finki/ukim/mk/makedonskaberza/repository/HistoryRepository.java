package mk.finki.ukim.mk.makedonskaberza.repository;

import mk.finki.ukim.mk.makedonskaberza.model.IssuerHistory;
import org.springframework.data.jpa.repository.JpaRepository;

import java.sql.Date;
import java.util.List;

public interface HistoryRepository extends JpaRepository<IssuerHistory, Integer> {
    public List<IssuerHistory> findByIssuerCodeOrderByEntryDateDesc(String code);
    public List<IssuerHistory> findByIssuerCodeAndEntryDateBetweenOrderByEntryDateDesc(String code, Date startDate, Date endDate);
}
