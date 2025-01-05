package mk.finki.ukim.mk.makedonskaberza.service.impl;

import mk.finki.ukim.mk.makedonskaberza.model.IssuerHistory;
import mk.finki.ukim.mk.makedonskaberza.repository.HistoryRepository;
import mk.finki.ukim.mk.makedonskaberza.service.HistoryService;
import mk.finki.ukim.mk.makedonskaberza.service.IssuerService;
import mk.finki.ukim.mk.makedonskaberza.service.strategy.context.HistoryServiceContext;
import org.springframework.stereotype.Service;

import java.sql.Date;
import java.util.ArrayList;
import java.util.List;

@Service
public class HistoryServiceImpl implements HistoryService {
    private final HistoryRepository repository;
    private final HistoryServiceContext context;
    private final List<String> validCodesForProjections;


    public HistoryServiceImpl(HistoryRepository repository, HistoryServiceContext context, IssuerService issuerService) {
        this.repository = repository;
        this.context = context;
        validCodesForProjections = issuerService.getAllIssuerCodes().stream()
                .filter(code -> repository.findIssuerHistoryByIssuerCodeIgnoreCase(code).size()>30).toList();

    }

    @Override
    public List<IssuerHistory> GetHistoryForCompany(String issuerCode, Date startDate, Date endDate) {
        return this.repository.findByIssuerCodeAndEntryDateBetweenOrderByEntryDateDesc(issuerCode, startDate, endDate);
    }

    @Override
    public IssuerHistory lastTransactionForIssuer(String code) {
        return repository.findFirstByIssuerCodeOrderByIdissuinghistoryDesc(code);
    }

    @Override
    public int numTransactionsLastYear(String code) {
        return (int) context.getTransactionsLastYearStrategy().countTransactions(code);

    }

    @Override
    public double avgMaxPrice(String code) {
        return Math.round(context.getAvgMaxPriceStrategy().calculate(code, "max") * 100.0) / 100.0;
    }

    @Override
    public double avgMinPrice(String code) {
        return Math.round(context.getAvgMinPriceStrategy().calculate(code, "min") * 100.0) / 100.0;
    }


    @Override
    public final List<String> codesForAnalysis(){
        return validCodesForProjections;
    }

    @Override
    public List<IssuerHistory> getTopCompanies(int count) {
        List<IssuerHistory> topComp = new ArrayList<>();
        topComp.add(repository.findIssuerHistoryByIssuerCodeIgnoreCase("alk").get(0));
        topComp.add(repository.findIssuerHistoryByIssuerCodeIgnoreCase("kmb").get(0));
        topComp.add(repository.findIssuerHistoryByIssuerCodeIgnoreCase("stb").get(0));
        topComp.add(repository.findIssuerHistoryByIssuerCodeIgnoreCase("ttk").get(0));
        topComp.add(repository.findIssuerHistoryByIssuerCodeIgnoreCase("tnb").get(0));
        topComp.add(repository.findIssuerHistoryByIssuerCodeIgnoreCase("mpt").get(0));

        return topComp;
    }





}
