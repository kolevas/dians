package mk.finki.ukim.mk.makedonskaberza.service;

import mk.finki.ukim.mk.makedonskaberza.model.IssuerHistory;

import java.sql.Date;
import java.util.List;
import java.util.Optional;

public interface HistoryService {
    public List<IssuerHistory> GetHistoryForCompany(String issuerCode);
    public List<IssuerHistory> GetHistoryForCompany(String issuerCode, Date startDate, Date endDate);
}
