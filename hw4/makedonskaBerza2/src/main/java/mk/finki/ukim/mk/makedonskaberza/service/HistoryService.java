package mk.finki.ukim.mk.makedonskaberza.service;

import mk.finki.ukim.mk.makedonskaberza.model.IssuerHistory;

import java.sql.Date;
import java.util.List;

public interface HistoryService {
    List<IssuerHistory> GetHistoryForCompany(String issuerCode, Date startDate, Date endDate);
    List<IssuerHistory> getTopCompanies(int count);
    IssuerHistory lastTransactionForIssuer(String code);
    int numTransactionsLastYear(String code);
    double avgMaxPrice(String code);
    double avgMinPrice(String code);

    List<String> codesForAnalysis();

}
