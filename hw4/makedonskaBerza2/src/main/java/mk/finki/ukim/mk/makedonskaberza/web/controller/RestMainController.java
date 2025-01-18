package mk.finki.ukim.mk.makedonskaberza.web.controller;


import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
public class RestMainController {

    private final RestTemplate restTemplate;

    @Value("${techanalysis.baseurl}")
    private String baseURL;

    private final String ANALYSIS_IMAGE_URL = baseURL + "/generate";
    private final String PREDICT_IMAGE_URL = baseURL + "/predict";



    public RestMainController(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @GetMapping("/get-flask-image")
    @ResponseBody
    public byte[] getImageFromFlask(@RequestParam String issuer, @RequestParam String interval, @RequestParam String prikaz) {
        String flaskUrlWithParams = ANALYSIS_IMAGE_URL + "?issuer=" + issuer + "&interval=" + interval + "&prikaz=" + prikaz;

        ResponseEntity<byte[]> response = restTemplate.getForEntity(flaskUrlWithParams, byte[].class);

        return response.getBody();
    }
    @GetMapping("/get-predicted-image")
    @ResponseBody
    public byte[] getImageFromPrediction(@RequestParam String issuer) {
        String flaskUrlWithParams = PREDICT_IMAGE_URL + "?issuer=" + issuer;

        ResponseEntity<byte[]> response = restTemplate.getForEntity(flaskUrlWithParams, byte[].class);

        return response.getBody();
    }

}