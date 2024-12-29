package mk.finki.ukim.mk.makedonskaberza.service.impl;

import mk.finki.ukim.mk.makedonskaberza.model.IssuerHistory;
import mk.finki.ukim.mk.makedonskaberza.repository.HistoryRepository;
import mk.finki.ukim.mk.makedonskaberza.service.HistoryService;
import mk.finki.ukim.mk.makedonskaberza.service.IssuerService;
import org.springframework.stereotype.Service;

import java.sql.Date;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
public class HistoryServiceImpl implements HistoryService {
    private final HistoryRepository repository;
    private final IssuerService issuerService;

    public HistoryServiceImpl(HistoryRepository repository, IssuerService issuerService) {
        this.repository = repository;
        this.issuerService = issuerService;
    }


    @Override
    public List<IssuerHistory> GetHistoryForCompany(String issuerCode) {
        return this.repository.findByIssuerCodeOrderByEntryDateDesc(issuerCode);
    }

    @Override
    public List<IssuerHistory> GetHistoryForCompany(String issuerCode, Date startDate, Date endDate) {
        return this.repository.findByIssuerCodeAndEntryDateBetweenOrderByEntryDateDesc(issuerCode, startDate, endDate);
    }
    @Override
    public List<IssuerHistory> GetIssuerHistoryByCode(String issuercode) {return repository.findIssuerHistoryByIssuerCodeIgnoreCase(issuercode);}

    @Override
    public IssuerHistory lastTransactionForIssuer(String code) {
        return repository.findFirstByIssuerCodeOrderByIdissuinghistoryDesc(code);
    }

    @Override
    public int numTransationslastyear(String code) {
        long count = repository.findIssuerHistoryByIssuerCodeIgnoreCase(code).stream()
                .filter(ih -> {
                    Date entryDate = ih.getEntryDate();
                    if (entryDate == null) {
                        return false;
                    }
                    LocalDateTime ihDate = entryDate.toLocalDate().atStartOfDay();
                    return ihDate.isAfter(LocalDateTime.now().minusYears(1));
                })
                .count();
        return (int) count;

    }

    @Override
    public double avgMaxPrice(String code){
        double max = repository.findIssuerHistoryByIssuerCodeIgnoreCase(code).stream()
                .filter(ih -> {
                    Date entryDate = ih.getEntryDate();
                    if (entryDate == null) {
                        return false;
                    }
                    LocalDateTime ihDate = entryDate.toLocalDate().atStartOfDay();
                    return ihDate.isAfter(LocalDateTime.now().minusYears(1));
                }).mapToDouble(IssuerHistory::getMaximumPrice).average().orElse(0);
        return  Math.round(max * 100.0) / 100.0;
    }

    @Override
    public double avgMinPrice(String code){
        double min = repository.findIssuerHistoryByIssuerCodeIgnoreCase(code).stream()
                .filter(ih -> {
                    Date entryDate = ih.getEntryDate();
                    if (entryDate == null) {
                        return false;
                    }
                    LocalDateTime ihDate = entryDate.toLocalDate().atStartOfDay();
                    return ihDate.isAfter(LocalDateTime.now().minusYears(1));
                }).mapToDouble(IssuerHistory::getMinimumPrice).average().orElse(0);
        return  Math.round(min * 100.0) / 100.0;
    }


    @Override
    public List<String> codesForAnalysis(){
        return issuerService.getAllIssuerCodes().stream()
                .filter(code -> repository.findIssuerHistoryByIssuerCodeIgnoreCase(code).size()>30).toList();
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
