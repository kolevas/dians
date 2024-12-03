package mk.finki.ukim.mk.makedonskaberza.repository;

import mk.finki.ukim.mk.makedonskaberza.model.Issuer;
import org.springframework.data.jpa.repository.JpaRepository;

public interface IssuerRepository extends JpaRepository<Issuer, String> {
}
