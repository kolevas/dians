package mk.finki.ukim.mk.makedonskaberza.service;

import mk.finki.ukim.mk.makedonskaberza.model.Issuer;
import mk.finki.ukim.mk.makedonskaberza.model.IssuerHistory;

import java.sql.Date;
import java.util.List;
import java.util.Optional;

public interface HistoryService {
    public List<IssuerHistory> GetHistoryForCompany(String issuerCode);
    public List<IssuerHistory> GetHistoryForCompany(String issuerCode, Date startDate, Date endDate);
    public List<IssuerHistory> getTopCompanies(int count);
    public List<IssuerHistory> GetIssuerHistoryByCode(String code);

    public IssuerHistory lastTransactionForIssuer(String code);
    public int numTransationslastyear(String code);
    public double avgMaxPrice(String code);
    public double avgMinPrice(String code);

}
