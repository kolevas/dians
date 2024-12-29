package mk.finki.ukim.mk.makedonskaberza.repository;

import mk.finki.ukim.mk.makedonskaberza.model.Issuer;
import mk.finki.ukim.mk.makedonskaberza.model.IssuerHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.awt.print.Pageable;
import java.sql.Date;
import java.util.List;

public interface HistoryRepository extends JpaRepository<IssuerHistory, Integer> {
    public List<IssuerHistory> findByIssuerCodeOrderByEntryDateDesc(String code);
    public List<IssuerHistory> findByIssuerCodeAndEntryDateBetweenOrderByEntryDateDesc(String code, Date startDate, Date endDate);

    @Query(
            value = "SELECT ih.* " +
                    "FROM issuinghistory ih " +
                    "INNER JOIN (" +
                    "    SELECT issuercode, MAX(avgprice) AS max_avg_price, MAX(idissuinghistory) AS latest_id " +  // Select latest unique id for tie-breaking
                    "    FROM issuinghistory " +
                    "    GROUP BY issuercode" +
                    ") grouped_issuers " +
                    "ON ih.issuercode = grouped_issuers.issuercode " +
                    "   AND ih.avgprice = grouped_issuers.max_avg_price " +
                    "   AND ih.idissuinghistory = grouped_issuers.latest_id " + // Match the unique ID for each group
                    "ORDER BY ih.avgprice DESC " +
                    "LIMIT 5",
            nativeQuery = true
    )
    List<IssuerHistory> findTop5AveragePriceByDistinctIssuers();



    public List<IssuerHistory> findIssuerHistoryByIssuerCodeIgnoreCase(String issuercode);
    public IssuerHistory findFirstByIssuerCodeOrderByIdissuinghistoryDesc(String code);
}
