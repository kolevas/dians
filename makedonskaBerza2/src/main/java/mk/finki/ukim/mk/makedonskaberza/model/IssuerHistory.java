package mk.finki.ukim.mk.makedonskaberza.model;


import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.sql.Date;

@Data
@Entity
@NoArgsConstructor
@Table(name="issuinghistory")
public class IssuerHistory {

    @Id
    private Integer idissuinghistory;
    @Column(name = "issuercode")
    private String issuerCode;
    @Column(name= "entrydate")
    private Date entryDate;
    @Column(name = "lasttransactionprice")
    private Double priceForLastTransaction;
    @Column(name = "maximumprice")
    private Double maximumPrice;
    @Column(name = "minimumprice")
    private Double minimumPrice;
    @Column(name = "avgprice")
    private Double averagePrice;
    @Column(name = "prompercent")
    private Double promPercent;
    private Integer quantity;
    @Column(name = "turnoverbest")
    private Double turnoverBEST;
    @Column(name = "turnovertotal")
    private Double totalTurnover;

//    @ManyToOne //tuka dodadov lista od issuers
//    @JoinColumn(name = "issuer_id", nullable = false)
//    private Issuer issuer;


    public IssuerHistory(String issuerCode, Date entryDate, Double priceForLastTransaction, Double maximumPrice, Double minimumPrice, Double averagePrice, Double promPercent, Integer quantity, Double turnoverBEST, Double totalTurnover) {
        this.issuerCode = issuerCode;
        this.entryDate = entryDate;
        this.priceForLastTransaction = priceForLastTransaction;
        this.maximumPrice = maximumPrice;
        this.minimumPrice = minimumPrice;
        this.averagePrice = averagePrice;
        this.promPercent = promPercent;
        this.quantity = quantity;
        this.turnoverBEST = turnoverBEST;
        this.totalTurnover = totalTurnover;
    }
}
