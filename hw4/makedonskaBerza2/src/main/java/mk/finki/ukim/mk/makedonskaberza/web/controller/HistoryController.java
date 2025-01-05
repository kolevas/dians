package mk.finki.ukim.mk.makedonskaberza.web.controller;

import mk.finki.ukim.mk.makedonskaberza.model.Issuer;
import mk.finki.ukim.mk.makedonskaberza.model.IssuerHistory;
import mk.finki.ukim.mk.makedonskaberza.service.HistoryService;
import mk.finki.ukim.mk.makedonskaberza.service.IssuerService;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.Date;
import java.util.List;

@Controller
@RequestMapping("/history")
public class HistoryController {
    private final HistoryService historyService;
    private final IssuerService issuerService;

    public HistoryController(HistoryService historyService, IssuerService issuerService) {
        this.historyService = historyService;
        this.issuerService = issuerService;
    }

    @GetMapping
    public String getTopIssuersByAveragePrice(@RequestParam(defaultValue = "5") int count, Model model) {
        List<IssuerHistory> issuersHistory = historyService.getTopCompanies(count);
        model.addAttribute("history", issuersHistory);
        return "index";
    }

    @GetMapping("/compare")
    public String companyComparison() {
        return "company_comparison";
    }

    @GetMapping("/get-comparison-info")
    public String comparisonInfo(@RequestParam String company1, @RequestParam String company2, Model model) {

        Issuer issuer1 = issuerService.GetIssuerByCode(company1);
        Issuer issuer2 = issuerService.GetIssuerByCode(company2);
        model.addAttribute("c1", company1.toUpperCase());
        model.addAttribute("c2", company2.toUpperCase());
        model.addAttribute("c1Max", historyService.avgMaxPrice(company1));
        model.addAttribute("c2Max", historyService.avgMaxPrice(company2));
        model.addAttribute("c1Min", historyService.avgMinPrice(company1));
        model.addAttribute("c2Min", historyService.avgMinPrice(company2));
        model.addAttribute("c1HV", issuer1.getHvTotal());
        model.addAttribute("c1Num", historyService.numTransactionsLastYear(company1));
        model.addAttribute("c2HV", issuer2.getHvTotal());
        model.addAttribute("c2Num", historyService.numTransactionsLastYear(company2));
        return "company_comparison";
    }


    @GetMapping("/report/{code}")
    public String reportDetails(@PathVariable String code, Model model) {

        Issuer issuer = issuerService.GetIssuerByCode(code);
        model.addAttribute("issuer", issuer);

        return "report_details";
    }

    @GetMapping("/issuer-history")
    public String issuerHistory(
            @RequestParam String issCode,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) Date startDate,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) Date endDate,
            Model model) {

        java.sql.Date start = java.sql.Date.valueOf(LocalDateTime.now().minusMonths(1).toLocalDate());
        java.sql.Date end = java.sql.Date.valueOf(LocalDateTime.now().toLocalDate());

        if (startDate != null) {
            start = new java.sql.Date(startDate.getTime());
        }
        if (endDate != null) {
            end = new java.sql.Date(endDate.getTime());
        }

        List<IssuerHistory> lastMonthHistory = historyService.GetHistoryForCompany(issCode, start, end);
        model.addAttribute("allHistory", lastMonthHistory);

        return "all_history";
    }

}
