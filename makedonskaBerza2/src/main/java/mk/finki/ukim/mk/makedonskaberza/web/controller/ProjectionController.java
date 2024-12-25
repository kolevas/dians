package mk.finki.ukim.mk.makedonskaberza.web.controller;


import mk.finki.ukim.mk.makedonskaberza.service.AnalysisService;
import mk.finki.ukim.mk.makedonskaberza.service.IssuerService;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Controller
@RequestMapping("/projection")
public class ProjectionController {

    private final IssuerService issuerService;
    private final AnalysisService analysisService;

    public ProjectionController(IssuerService issuerService, AnalysisService analysisService) {
        this.issuerService = issuerService;
        this.analysisService = analysisService;
    }

    @GetMapping
    public String getProjectionsPage(Model model) {
        String value="/img/ADIN.png";
        List<String> optionsIssuer=issuerService.getAllIssuerCodes();
        List<String> prikazi = analysisService.getPrikazi();
        List<String> intervali = analysisService.getVreminja();
        model.addAttribute("optionsIssuer", optionsIssuer);
        model.addAttribute("prikazi", prikazi);
        model.addAttribute("intervali", intervali);
        model.addAttribute("imageID", value);
        return "projections";
    }




    @PostMapping
    public String getProjections(@RequestParam String issuer,
                                 @RequestParam String prikaz,
                                 @RequestParam String interval,
                                 Model model) {
        String path = "/img/" + issuer + ".png";
        try {
            // Call service to generate the image
            analysisService.getImg(issuer, prikaz, interval);
        } catch (Exception e) {
            // Log the error and show a meaningful message to the user
            model.addAttribute("error", "Не можевме да ја генерираме проекцијата за " + issuer + ". Обиди се повторно.");
            e.printStackTrace();
            return "projections";
        }

        // Fetch additional options
        List<String> optionsIssuer = issuerService.getAllIssuerCodes();
        List<String> prikazi = analysisService.getPrikazi();
        List<String> intervali = analysisService.getVreminja();

        // Add attributes to the model
        model.addAttribute("optionsIssuer", optionsIssuer);
        model.addAttribute("prikazi", prikazi);
        model.addAttribute("intervali", intervali);
        model.addAttribute("imageID", path);
        model.addAttribute("advice", "Инвестирај во " + issuer);

        return "projections";
    }

}