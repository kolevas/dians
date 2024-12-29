package mk.finki.ukim.mk.makedonskaberza.web.controller;

import jakarta.servlet.http.HttpServletRequest;
import mk.finki.ukim.mk.makedonskaberza.model.Issuer;
import mk.finki.ukim.mk.makedonskaberza.model.IssuerHistory;
import mk.finki.ukim.mk.makedonskaberza.service.HistoryService;
import mk.finki.ukim.mk.makedonskaberza.service.IssuerService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

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

    @GetMapping("/rezultati-prebaruvanje")
    public String rezultatiPrebaruvanje(@RequestParam(required = false) String searchName,
                                        Model model) {
        List<Issuer> companies = issuerService.searchResult(searchName);
        model.addAttribute("companies", companies);
        return "rezultati-prebaruvanje";
    }


    @GetMapping("/detali-kompanija/{code}")
    public String detali_kompanija(@PathVariable String code, HttpServletRequest request, Model model) {
        List<IssuerHistory> issuerHistory = historyService.GetIssuerHistoryByCode(code);
        Issuer issuer = issuerService.GetIssuerByCode(code);

        model.addAttribute("issuer", issuer);
        model.addAttribute("history", historyService.lastTransactionForIssuer(code));

        //za podatoci za poslednata godina (treba da se dodade samo vo html, kako kaj sporedba slicno)

        String imagePath = "/img/stock_prediction_graph.png";

        try {
            issuerService.pricePredictionImage(code);
        } catch (Exception e) {
            model.addAttribute("error", "Не можевме да ја генерираме проекцијата за " + code + ". Обиди се повторно.");
            e.printStackTrace();
            return "detali-kompanija";
        }
        model.addAttribute("imageID", imagePath);
        Issuer issuer1 = issuerService.GetIssuerByCode(code);
        model.addAttribute("c1",code.toUpperCase());
        model.addAttribute("c1Max", historyService.avgMaxPrice(code));
        model.addAttribute("c1Min", historyService.avgMinPrice(code));
        model.addAttribute("c1HV", issuer1.getHvTotal());
        model.addAttribute("c1Num", historyService.numTransationslastyear(code));
        return "detali-kompanija";
    }
//    @PostMapping("/detali-kompanija/{code}")
//    public String getStockPredictionImage(@PathVariable String code,
//                                          Model model) {
//        String imagePath = "/img/stock_prediction.png";
//
//        try {
//            issuerService.pricePredictionImage(code);
//        } catch (Exception e) {
//            model.addAttribute("error", "Не можевме да ја генерираме проекцијата за " + code + ". Обиди се повторно.");
//            e.printStackTrace();
//            return "detali-kompanija";
//        }
//
//        // Fetch additional company details
//        Issuer companyDetails = issuerService.GetIssuerByCode(code);
//        if (companyDetails == null) {
//            model.addAttribute("error", "Компанијата со шифра " + code + " не постои.");
//            return "detali-kompanija";
//        }
//
//        // Add attributes to the model for rendering the page
//        model.addAttribute("companyDetails", companyDetails);
//        model.addAttribute("imageID", imagePath); // Add the generated image path to the model
//
//        return "detali-kompanija"; // Return the updated details page
//    }


}
