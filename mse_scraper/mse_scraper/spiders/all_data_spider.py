import csv
import json
import os

import psycopg2

import scrapy
from datetime import datetime


class AllDataSpider(scrapy.Spider):
    name = "all_data_spider"
    start_urls = ["https://www.mse.mk/mk/stats/symbolhistory/%7B%7D"]  # Replace with your target URL

    def __init__(self, *args, **kwargs):
        super(AllDataSpider, self).__init__(*args, **kwargs)
        # Calculate the current year
        self.current_year = datetime.now().year
        self.from_date = datetime.now().strftime("%d.%m.%Y")
        self.to_date = datetime.now().strftime("%d.%m.%Y")

    def start_requests(self):
        # POST request payload
        payload = {
            "FromDate": self.from_date,
            "ToDate": self.to_date,
            "Code": "123"  # Replace or generate dynamically as needed
        }

        # Send POST request
        yield scrapy.Request(
            url=self.start_urls[0],
            method="POST",
            body=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            callback=self.parse
        )

    def parse(self, response):
        # Extract all 'value' attributes from the <select name="Code">
        values = response.xpath('//select[@name="Code"]/option/@value').getall()

        # values = [s for s in values if s.isalpha()]
        values = [s for s in values if s == 'TTK']
        for year in range(self.current_year - 10, self.current_year + 1):  # Last 10 years
            print(f'CRAWLING {year}')
            self.from_date = datetime(year, 1, 1).strftime("%d.%m.%Y")  # January 1st of the current year
            self.to_date = datetime(year, 12, 31).strftime("%d.%m.%Y")  # December 31st of the current year

            # Make a POST request for each value
            for value in values:
                payload = {
                    "FromDate": self.from_date,
                    "ToDate": self.to_date,
                    "Code": value
                }

                # Yield a POST request
                yield scrapy.Request(
                    url="https://www.mse.mk/mk/stats/symbolhistory/%7B%7D",  # Replace with your POST URL
                    method="POST",
                    body=json.dumps(payload),
                    headers={"Content-Type": "application/json"},
                    callback=self.parse_post_response,
                    meta={"code": value, "year": year}  # Pass the value to the callback for context
                )

    def parse_post_response(self, response):
        # Get the code from meta
        content_type = response.headers.get('Content-Type', '').decode('utf-8')

        if 'html' not in content_type:
            return
        code = response.meta["code"]

        # Extract the table rows from the HTML
        table = response.xpath('//*[contains(@id, "resultsTable")]')

        headers = table.xpath('./thead/tr/th/text()').getall()
        rows = table.xpath('./tbody/tr')

        new_headers = []

        for header in headers:
            trimmed = header.strip()
            new_headers.append(trimmed)

        extracted_data = []
        for row in rows:
            # Extract all cell values in the row
            cells = row.xpath('./td/text()').getall()
            extracted_data.append(cells)

        self.insert_to_db(code, extracted_data)

    @staticmethod
    def save_to_csv(code, headers, rows, year):
        # Ensure the output directory exists
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        # Define the output file path
        file_path = os.path.join(output_dir, f"{code}_{year}.csv")

        # Write the data to the CSV file
        with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            # Write headers
            writer.writerow(headers)
            # Write rows
            writer.writerows(rows)

    @staticmethod
    def insert_to_db(code, rows):
        conn = psycopg2.connect(database="mse",
                                user="mse_owner",
                                password="CYXP4fDEiH5g",
                                host='ep-bold-dream-a2fi281z.eu-central-1.aws.neon.tech',
                                port=5432)

        data = []

        if not (rows and rows[0] and rows[0][0]):
            return

        print(f'{datetime.now().time()} | INSERTING DATA FOR {code} FOR DATE {rows[0][0]} | LENGTH: {len(rows)}')
        for row in rows:
            # Convert the string to a datetime object
            date_obj = datetime.strptime(row[0], "%d.%m.%Y")

            # Reformat the datetime object to the new format
            row[0] = date_obj.strftime("%Y-%m-%d")
            row.extend([-1.00] * (9 - len(row)))
            for i in range(1, 9):
                if isinstance(row[i], str):
                    tmp = row[i].replace('.', '').replace(',', '.')
                    row[i] = float(tmp)

            if not isinstance(row[6], int):
                row[6] = int(row[6])

            data.append((code, *row))

        cur = conn.cursor()
        cur.execute(
            "CALL add_issuing_history_data(ARRAY[%s]::tt_issuing_history_entry[]);",
            (data,)
        )

        conn.commit()  # This is mandatory because we want to commit changes to DB
        cur.close()
        conn.close()
