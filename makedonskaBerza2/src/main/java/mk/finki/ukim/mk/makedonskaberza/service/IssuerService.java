package mk.finki.ukim.mk.makedonskaberza.service;

import mk.finki.ukim.mk.makedonskaberza.model.Issuer;

import java.util.List;

public interface IssuerService {
    List<Issuer> GetAllIssuers();
    List<Issuer> searchCompanies(String text);
    Issuer GetIssuerByCode(String code);
    List<Issuer> searchResult(String search);
    List<Issuer> searchByCode(String code);
    List<String> getAllIssuerCodes();

    void pricePredictionImage(String issuer);

}
