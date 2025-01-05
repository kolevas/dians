package mk.finki.ukim.mk.makedonskaberza.bootstrap;

import jakarta.annotation.PostConstruct;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class CSVToDatabase {

    @PostConstruct
    public static void main(String[] args) {
        String jdbcURL = "jdbc:h2:./data/testdb;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE";  // File-based H2 Database URL
        String username = "sa";
        String password = "password";
        String csvFile = "C:\\Users\\private\\Desktop\\all_issuer_data.csv";  // Path to your CSV file

        // Database connection
        try (Connection connection = DriverManager.getConnection(jdbcURL, username, password)) {

            // Create a table for issuers (adjust schema based on your CSV)
            String createTableQuery = "CREATE TABLE IF NOT EXISTS issuers ("
                    + "code VARCHAR(255) PRIMARY KEY, "
                    + "name VARCHAR(255), "
                    + "address VARCHAR(255), "
                    + "city VARCHAR(255), "
                    + "email VARCHAR(255), "
                    + "web_page VARCHAR(255), "
                    + "contact_person VARCHAR(255), "
                    + "phone VARCHAR(50), "
                    + "company_profile TEXT, "
                    + "total_revenue_2023 DECIMAL(15, 2), "
                    + "profit_before_tax DECIMAL(15, 2), "
                    + "equity DECIMAL(15, 2), "
                    + "total_liabilities DECIMAL(15, 2), "
                    + "total_assets DECIMAL(15, 2), "
                    + "market_capitalization DECIMAL(15, 2), "
                    + "hv_isin VARCHAR(255), "
                    + "hv_total DECIMAL(15, 2))";  // Adjust the data types as needed
            connection.createStatement().execute(createTableQuery);

            // Read CSV file and insert data into the database
            try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {
                String line;
                // Skip header row
                br.readLine();  // Assuming the first line is the header

                while ((line = br.readLine()) != null) {
                    String[] fields = line.split(",");

                    // Insert data into the issuers table
                    String insertQuery = "INSERT INTO issuers (code, name, address, city, email, web_page, contact_person, "
                            + "phone, company_profile, total_revenue_2023, profit_before_tax, equity, total_liabilities, "
                            + "total_assets, market_capitalization, hv_isin, hv_total) "
                            + "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
                    try (PreparedStatement statement = connection.prepareStatement(insertQuery)) {
                        statement.setString(1, fields[0]);  // code
                        statement.setString(2, fields[1]);  // name
                        statement.setString(3, fields[2]);  // address
                        statement.setString(4, fields[3]);  // city
                        statement.setString(5, fields[4]);  // email
                        statement.setString(6, fields[5]);  // web_page
                        statement.setString(7, fields[6]);  // contact_person
                        statement.setString(8, fields[7]);  // phone
                        statement.setString(9, fields[8]);  // company_profile
                        statement.setBigDecimal(10, new java.math.BigDecimal(fields[9]));  // total_revenue_2023
                        statement.setBigDecimal(11, new java.math.BigDecimal(fields[10]));  // profit_before_tax
                        statement.setBigDecimal(12, new java.math.BigDecimal(fields[11]));  // equity
                        statement.setBigDecimal(13, new java.math.BigDecimal(fields[12]));  // total_liabilities
                        statement.setBigDecimal(14, new java.math.BigDecimal(fields[13]));  // total_assets
                        statement.setBigDecimal(15, new java.math.BigDecimal(fields[14]));  // market_capitalization
                        statement.setString(16, fields[15]);  // hv_isin
                        statement.setBigDecimal(17, new java.math.BigDecimal(fields[16]));  // hv_total
                        statement.executeUpdate();
                    }
                }
            }

            System.out.println("Data inserted successfully.");
        } catch (SQLException | IOException e) {
            e.printStackTrace();
        }
    }
}
