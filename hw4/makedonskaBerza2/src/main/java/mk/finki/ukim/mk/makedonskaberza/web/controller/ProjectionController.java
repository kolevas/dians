package mk.finki.ukim.mk.makedonskaberza.web.controller;


import mk.finki.ukim.mk.makedonskaberza.service.AnalysisService;
import mk.finki.ukim.mk.makedonskaberza.service.HistoryService;
import mk.finki.ukim.mk.makedonskaberza.service.IssuerService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.Base64;
import java.util.Date;
import java.util.List;

@Controller
@RequestMapping("/projection")
public class ProjectionController {


    private final AnalysisService analysisService;
    private final IssuerService issuerService;
    private final HistoryService historyService;

    public ProjectionController(AnalysisService analysisService, IssuerService issuerService, HistoryService historyService) {
        this.analysisService = analysisService;
        this.issuerService = issuerService;
        this.historyService = historyService;
    }

    @GetMapping
    public String getProjectionsPage(Model model) {
        List<String> optionsIssuer= historyService.codesForAnalysis();
        List<String> prikazi = analysisService.getParams();
        List<String> intervals = analysisService.getIntervals();
        model.addAttribute("optionsIssuer", optionsIssuer);
        model.addAttribute("prikazi",    prikazi);
        model.addAttribute("intervali", intervals);
        return "projections";
    }




    @PostMapping
    public String getProjections(@RequestParam String issuer,
                                 @RequestParam String prikaz,
                                 @RequestParam String interval,
                                 Model model) throws IOException {
        InputStream imgId;
        try {
            imgId = analysisService.getImg(issuer, prikaz, interval);
        } catch (Exception e) {
            model.addAttribute("error", "Не можевме да ја генерираме проекцијата за " + issuer + ". Обиди се повторно.");
            return "projections";
        }

        byte[] imageBytes = imgId.readAllBytes();
        String base64Image = Base64.getEncoder().encodeToString(imageBytes);
        model.addAttribute("base64Image", base64Image);

        List<String> optionsIssuer = issuerService.getAllIssuerCodes();
        List<String> prikazi = analysisService.getParams();
        List<String> intervali = analysisService.getIntervals();

        SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMddHHmmss");
        String formattedDate = sdf.format(new Date());

        model.addAttribute("optionsIssuer", optionsIssuer);
        model.addAttribute("prikazi", prikazi);
        model.addAttribute("intervali", intervali);
        model.addAttribute("advice", "Инвестирај во " + issuer);
        model.addAttribute("timestamp", formattedDate);
        return "projections";
    }

}