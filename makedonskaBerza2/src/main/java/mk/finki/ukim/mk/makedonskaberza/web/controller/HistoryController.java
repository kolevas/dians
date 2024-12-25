package mk.finki.ukim.mk.makedonskaberza.web.controller;

import jakarta.servlet.http.HttpServletRequest;
import mk.finki.ukim.mk.makedonskaberza.model.Issuer;
import mk.finki.ukim.mk.makedonskaberza.model.IssuerHistory;
import mk.finki.ukim.mk.makedonskaberza.service.HistoryService;
import mk.finki.ukim.mk.makedonskaberza.service.IssuerService;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.time.ZoneId;
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
        List<IssuerHistory> issuersHistory = historyService.getTopCompanies(count);  // Повик на сервисот
        model.addAttribute("history", issuersHistory);  // Проследување на податоците во моделот
        return "index";  // Враќање на главната страница (Thymeleaf шаблон)
    }

    @GetMapping("/sporedi")
    public String sporedba(HttpServletRequest request) {
        return "sporedba-kompanii";
    }

    @GetMapping("/zemi-info-sporedba")
    public String infoZaSporedba(@RequestParam String company1, @RequestParam String company2, Model model){

        Issuer issuer1 = issuerService.GetIssuerByCode(company1);
        Issuer issuer2 = issuerService.GetIssuerByCode(company2);
        model.addAttribute("c1",company1.toUpperCase());
        model.addAttribute("c2",company2.toUpperCase());
        model.addAttribute("c1Max", historyService.avgMaxPrice(company1));
        model.addAttribute("c2Max", historyService.avgMaxPrice(company2));
        model.addAttribute("c1Min", historyService.avgMinPrice(company1));
        model.addAttribute("c2Min", historyService.avgMinPrice(company2));
        model.addAttribute("c1HV", issuer1.getHvTotal());
        model.addAttribute("c1Num", historyService.numTransationslastyear(company1));
        model.addAttribute("c2HV", issuer2.getHvTotal());
        model.addAttribute("c2Num", historyService.numTransationslastyear(company2));
        return "sporedba-kompanii";
    }


    @GetMapping("/detali-izvestaj/{code}")
    public String detaliIzvaestaj(@PathVariable String code, HttpServletRequest request, Model model) {

        Issuer issuer = issuerService.GetIssuerByCode(code);
        model.addAttribute("issuer", issuer);

        return "detali-izvestaj";
    }

    @GetMapping("/istorija-izdavac")
    public String istIzdavac(
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

        return "cela-istorija";
    }

}
