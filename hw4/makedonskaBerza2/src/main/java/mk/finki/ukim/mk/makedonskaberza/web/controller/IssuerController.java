package mk.finki.ukim.mk.makedonskaberza.web.controller;

import mk.finki.ukim.mk.makedonskaberza.model.Issuer;
import mk.finki.ukim.mk.makedonskaberza.service.HistoryService;
import mk.finki.ukim.mk.makedonskaberza.service.IssuerService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.List;

@Controller
@RequestMapping("/issuer")
public class IssuerController {
    private final IssuerService issuerService;
    private final HistoryService historyService;

    public IssuerController(IssuerService issuerService, HistoryService historyService) {
        this.issuerService = issuerService;
        this.historyService = historyService;
    }

    @GetMapping("/search-results")
    public String searchResults(@RequestParam(required = false) String searchName,
                                        Model model) {
        List<Issuer> companies = issuerService.searchResult(searchName);
        model.addAttribute("companies", companies);
        return "search_results";
    }


    @GetMapping("/company-details/{code}")
    public String companyDetails(@PathVariable String code, Model model){
        Issuer issuer1 = issuerService.GetIssuerByCode(code);
        model.addAttribute("issuer", issuer1);
        model.addAttribute("history", historyService.lastTransactionForIssuer(code));
        model.addAttribute("c1",code.toUpperCase());
        model.addAttribute("c1Max", historyService.avgMaxPrice(code));
        model.addAttribute("c1Min", historyService.avgMinPrice(code));
        model.addAttribute("c1HV", issuer1.getHvTotal());
        model.addAttribute("c1Num", historyService.numTransactionsLastYear(code));
        return "company_details";
    }

    @GetMapping("/company-details/predict/{code}")
    public String pricePrediction(@PathVariable String code, Model model) throws IOException {
        Issuer issuer = issuerService.GetIssuerByCode(code);

        model.addAttribute("issuer", issuer);
        model.addAttribute("history", historyService.lastTransactionForIssuer(code));

        //za podatoci za poslednata godina (treba da se dodade samo vo html, kako kaj sporedba slicno)

            InputStream imageInput;
        try {
                imageInput = issuerService.pricePredictionImage(code);
                } catch (Exception e) {
                model.addAttribute("error", "Не можевме да ја генерираме проекцијата за " + code + ". Обиди се повторно.");

                return String.format("redirect:/company-details/{%s}",code);
                }

                byte[] imageBytes = imageInput.readAllBytes();
                String base64Image = Base64.getEncoder().encodeToString(imageBytes);
                model.addAttribute("base64Image", base64Image);

        Issuer issuer1 = issuerService.GetIssuerByCode(code);
        model.addAttribute("c1",code.toUpperCase());
        model.addAttribute("c1Max", historyService.avgMaxPrice(code));
        model.addAttribute("c1Min", historyService.avgMinPrice(code));
        model.addAttribute("c1HV", issuer1.getHvTotal());
        model.addAttribute("c1Num", historyService.numTransactionsLastYear(code));
        return "company_details";
    }

}

//    InputStream imageInput;
//        try {
//                imageInput = issuerService.pricePredictionImage(code);
//                } catch (Exception e) {
//                model.addAttribute("error", "Не можевме да ја генерираме проекцијата за " + code + ". Обиди се повторно.");
//
//                return String.format("redirect:/company-details/{%s}",code);
//                }
////
//                String imgId = String.format("%s_prediction_graph.png", code);
//                Path imgPath = Paths.get("src/main/resources/static/images", imgId);
//                byte[] imageBytes = imageInput.readAllBytes();
//                String base64Image = Base64.getEncoder().encodeToString(imageBytes);
//                model.addAttribute("base64Image", base64Image);