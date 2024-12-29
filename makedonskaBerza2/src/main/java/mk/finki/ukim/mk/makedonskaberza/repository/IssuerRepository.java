package mk.finki.ukim.mk.makedonskaberza.repository;

import mk.finki.ukim.mk.makedonskaberza.model.Issuer;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface IssuerRepository extends JpaRepository<Issuer, String> {
    public List<Issuer> findByIssuernameContainingIgnoreCase(String issuername);
    public List<Issuer> findByIssuercodeContainingIgnoreCase(String issuercode);
    public Issuer findByIssuercodeIgnoreCase (String iss);

    public List<Issuer> findAllByIssuercodeContainingIgnoreCaseOrIssuernameContainingIgnoreCase(String s1, String s2);


}
