package mk.finki.ukim.mk.makedonskaberza.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Entity
@NoArgsConstructor
@Table(name="issuers")
public class Issuer {

    @Id
    private String issuercode;
    private String issuername;
    private String address;
    private String city;
    private String email;
    @Column(name = "web_page")
    private String webpage;
    @Column(name = "contact_person")
    private String contactPerson;
    private String contact_phone;
    @Column(name = "company_profile")
    private String companyProfile;
    @Column(name = "total_revenue_2023")
    private float totalRevenueLastYear;
    @Column(name = "profit_before_tax")
    private float profitAfterTax;
    private float equity;
    @Column(name = "total_liablilities")
    private float totalLiabilities;
    @Column(name = "total_assets")
    private float totalAssets;
    @Column(name = "market_capitalization")
    private float marketCapitalization;
    @Column(name = "hv_isin")
    private String hvIsin;
    @Column(name = "hv_total")
    private float hvTotal;

    public Issuer(String name, String address, String city, String email, String webPage, String contactPerson, String phone, String companyProfile, float totalRevenue2023, float profitBeforeTax, float equity, float totalLiabilities, float totalAssets, float marketCapitalization, String hvIsin, float hvTotal) {
        this.issuername = name;
        this.address = address;
        this.city = city;
        this.email = email;
        this.webpage = webPage;
        this.contactPerson = contactPerson;
        this.contact_phone = phone;
        this.companyProfile = companyProfile;
        this.totalRevenueLastYear = totalRevenue2023;
        this.profitAfterTax = profitBeforeTax;
        this.equity = equity;
        this.totalLiabilities = totalLiabilities;
        this.totalAssets = totalAssets;
        this.marketCapitalization = marketCapitalization;
        this.hvIsin = hvIsin;
        this.hvTotal = hvTotal;
    }




}
