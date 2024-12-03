package mk.finki.ukim.mk.makedonskaberza.web.controller;

import mk.finki.ukim.mk.makedonskaberza.model.Issuer;
import mk.finki.ukim.mk.makedonskaberza.service.IssuerService;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

@Controller
@RequestMapping("/issuer")
public class IssuerController {
    private final IssuerService issuerService;

    public IssuerController(IssuerService issuerService) {
        this.issuerService = issuerService;
    }

    @GetMapping
    public ResponseEntity<List<Issuer>> getHomePage() {
        return ResponseEntity.ok(this.issuerService.GetAllIssuers());
    }
}
