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
        print(
            "-------------------------------------------VALUES-----------------------------------------------------------------------------------------------------------------")
        values = [s for s in values if s.isalpha()]
        print(values)

        conn = psycopg2.connect(
            database="mse",
            user="mse_owner",
            password="CYXP4fDEiH5g",
            host="ep-bold-dream-a2fi281z.eu-central-1.aws.neon.tech",
            port=5432
        )
        cur = conn.cursor()

        cur.execute("SELECT get_last_date_from_history_data()")
        self.from_date=cur.fetchone()[0]

        self.log(f"CRAWLING FROM {self.from_date} TO {self.to_date}")

        for value in values:
            payload = {
                "FromDate": self.from_date,
                "ToDate": self.to_date,
                "Code": value
            }

            yield scrapy.Request(
                url=f"https://www.mse.mk/mk/symbol/{value}",  # Replace with your POST URL
                method="GET",
                body=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                callback=self.parse_issuer_response,
                meta={"code": value}
            )

    def parse_issuer_response(self, response):
        # Extract additional data
        code = response.meta["code"]

        title = response.xpath('//*[@id="izdavach"]/div[1]/div[2]/text()').get()

        if(title is None):
            self.log(f"NO DATA FOR CODE {code}")
            return

        address = response.xpath('//*[@id="izdavach"]/div[3]/div[2]/text()').get()
        city = response.xpath('//*[@id="izdavach"]/div[4]/div[2]/text()').get()
        email = response.xpath('//*[@id="izdavach"]/div[6]/div[2]/text()').get()
        web_page = response.xpath('//*[@id="izdavach"]/div[7]/div[2]/a/@href').get()
        contact_person = response.xpath('//*[@id="izdavach"]/div[8]/div[2]/span/text()').get()
        contact_phone = response.xpath('// *[ @ id = "izdavach"] / div[9] / div[2]/text()').get()
        details_list = response.xpath('//*[@id="companyProfile"]/p/text()').getall()
        self.log(f"DETAILS LIST: {details_list}")
        company_profile = '\n'.join(details_list)
        total_revenue_2023 = float(response.xpath('//*[@id="red10"]/td[2]/text()').get(default="-1.0").replace('.', '').replace(',', '.'))
        profit_before_tax = float(response.xpath('//*[@id="red11"]/td[2]/text()').get(default="-1.0").replace('.', '').replace(',', '.'))
        equity = float(response.xpath('//*[@id="red12"]/td[2]/text()').get(default="-1.0").replace('.', '').replace(',', '.'))
        total_liablilities = float(response.xpath('//*[@id="red13"]/td[2]/text()').get(default="-1.0").replace('.', '').replace(',', '.'))
        total_assets = float(response.xpath('//*[@id="red14"]/td[2]/text()').get(default="-1.0").replace('.', '').replace(',', '.'))
        market_capitalization = float(response.xpath('//*[@id="red15"]/td[2]/text()').get(default="-1.0").replace('.', '').replace(',', '.'))
        hv_isin = response.xpath('//*[@id="symbol-data"]/div[2]/div[2]/text()').get(default="-1.0")
        hv_total = float(response.xpath('//*[@id="symbol-data"]/div[3]/div[2]/text()').get(default="-1.0").replace('.', '').replace(',', '.'))

        issuer_data = [title,
                        address,
                        city,
                        email,
                        web_page,
                        contact_person,
                        contact_phone,
                        company_profile,
                        total_revenue_2023,
                        profit_before_tax,
                        equity,
                        total_liablilities,
                        total_assets,
                        market_capitalization,
                        hv_isin,
                        hv_total]

        # Pass additional data to the next request
        payload = {
            "FromDate": self.from_date,
            "ToDate": self.to_date,
            "Code": code
        }

        yield scrapy.Request(
            url="https://www.mse.mk/mk/stats/symbolhistory/%7B%7D",  # Replace with your POST URL
            method="POST",
            body=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            callback=self.parse_post_response,
            meta={"code": code, "issuer_data": issuer_data}
        )

    def parse_post_response(self, response):
        content_type = response.headers.get('Content-Type', '').decode('utf-8')
        if 'html' not in content_type:
            return

        code = response.meta["code"]
        issuer_data = response.meta["issuer_data"]

        self.log(f"ISSUER DATA: {issuer_data}")

        table = response.xpath('//*[contains(@id, "resultsTable")]')
        rows = table.xpath('./tbody/tr')

        for row in rows:
            cells = row.xpath('./td/text()').getall()
            self.all_data.append((issuer_data, code, cells))  # Aggregate the data

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

        for issuer_data, code, row in self.all_data:
            # Process the row before inserting
            row_copy = row
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
                print(row)
                data.append((issuer_data, (code, *row)))

        if data:
            for company in data:
                print(f"Inserting {company[0]} issuer into the database.")
                print(f"Inserting {len(company[1])} records into the database.")
                cur.execute(
                    "CALL add_issuing_history_data(%s::tt_issuer_entry, ARRAY[%s]::tt_issuing_history_entry[]);",
                    ((company[1][0], *company[0]), company[1],)
                )
                conn.commit()

        cur.close()
        conn.close()