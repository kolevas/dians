package mk.finki.ukim.mk.makedonskaberza.web.controller;

import mk.finki.ukim.mk.makedonskaberza.model.IssuerHistory;
import mk.finki.ukim.mk.makedonskaberza.service.HistoryService;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.Date;
import java.util.List;

@Controller
@RequestMapping("/history")
public class HistoryController {
    private final HistoryService historyService;

    public HistoryController(HistoryService historyService) {
        this.historyService = historyService;
    }

    @GetMapping("{code}")
    public ResponseEntity<List<IssuerHistory>> getHistoryForCompany(
            @PathVariable String code,
            @RequestParam(required = false) @DateTimeFormat(pattern = "yyyy-MM-dd") Date startDate,
            @RequestParam(required = false) @DateTimeFormat(pattern = "yyyy-MM-dd") Date endDate) {

        java.sql.Date sqlStartDate = null;
        java.sql.Date sqlEndDate = null;

        if (startDate != null) {
            sqlStartDate = new java.sql.Date(startDate.getTime());
        }
        if (endDate != null) {
            sqlEndDate = new java.sql.Date(endDate.getTime());
        }

        if (sqlStartDate == null || sqlEndDate == null) {
            return ResponseEntity.ok(this.historyService.GetHistoryForCompany(code));
        }

        System.out.println("----------------------startDate");
        System.out.println(sqlStartDate);


        System.out.println("----------------------startDate");
        System.out.println(sqlEndDate);

        return ResponseEntity.ok(this.historyService.GetHistoryForCompany(code, sqlStartDate, sqlEndDate));
    }

}
