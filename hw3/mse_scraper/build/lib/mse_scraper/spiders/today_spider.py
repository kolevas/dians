import csv
import json
import os
from datetime import datetime

import psycopg2
import scrapy


class TodaySpider(scrapy.Spider):
    name = "today_spider"
    start_urls = ["https://www.mse.mk/mk/stats/symbolhistory/%7B%7D"]  # Replace with your target URL

    def __init__(self, *args, **kwargs):
        super(TodaySpider, self).__init__(*args, **kwargs)
        self.from_date = datetime.now().strftime("%d.%m.%Y")
        self.to_date = datetime.now().strftime("%d.%m.%Y")
        self.all_data = []  # Aggregate all scraped data

    def start_requests(self):
        payload = {
            "FromDate": self.from_date,
            "ToDate": self.to_date,
            "Code": "123"  # Replace or generate dynamically as needed
        }

        yield scrapy.Request(
            url=self.start_urls[0],
            method="POST",
            body=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            callback=self.parse
        )

    def parse(self, response):
        values = response.xpath('//select[@name="Code"]/option/@value').getall()
        values = [s for s in values if s.isalpha()]

        print(f'CRAWLING TODAY')

        for value in values:
            payload = {
                "FromDate": self.from_date,
                "ToDate": self.to_date,
                "Code": value
            }

            yield scrapy.Request(
                url="https://www.mse.mk/mk/stats/symbolhistory/%7B%7D",  # Replace with your POST URL
                method="POST",
                body=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                callback=self.parse_post_response,
                meta={"code": value}
            )

    def parse_post_response(self, response):
        content_type = response.headers.get('Content-Type', '').decode('utf-8')
        if 'html' not in content_type:
            return

        code = response.meta["code"]

        table = response.xpath('//*[contains(@id, "resultsTable")]')
        rows = table.xpath('./tbody/tr')

        for row in rows:
            cells = row.xpath('./td/text()').getall()
            self.all_data.append((code, cells))  # Aggregate the data

    def closed(self, reason):
        # Save to DB after all scraping is complete
        self.insert_all_to_db()

    def insert_all_to_db(self):
        if not self.all_data:
            print("No data to insert.")
            return

        conn = psycopg2.connect(
            database="mse",
            user="mse_owner",
            password="CYXP4fDEiH5g",
            host="ep-bold-dream-a2fi281z.eu-central-1.aws.neon.tech",
            port=5432
        )
        cur = conn.cursor()
        data = []

        for code, row in self.all_data:
            # Process the row before inserting
            if row and row[0]:
                try:
                    date_obj = datetime.strptime(row[0], "%d.%m.%Y")
                    row[0] = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    continue

                row.extend([-1.00] * (9 - len(row)))
                for i in range(1, 9):
                    if isinstance(row[i], str):
                        tmp = row[i].replace('.', '').replace(',', '.')
                        row[i] = float(tmp)

                if not isinstance(row[6], int):
                    row[6] = int(row[6])

                data.append((code, *row))

        if data:
            print(f"Inserting {len(data)} records into the database.")
            cur.execute(
                "CALL add_issuing_history_data(ARRAY[%s]::tt_issuing_history_entry[]);",
                (data,)
            )
            conn.commit()

        cur.close()
        conn.close()