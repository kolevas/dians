import os
from gc import collect

import pandas as pd
import requests
from bs4 import BeautifulSoup as BS
from concurrent.futures import ThreadPoolExecutor

BASE_URL_HISTORY = "https://www.mse.mk/mk/stats/symbolhistory/{}"
BASE_URL_DATA = "https://www.mse.mk/mk/symbol/{}"
DATA_DIR = "issuer_data"

# Ensure the directory for issuer data exists
os.makedirs(DATA_DIR, exist_ok=True)


def get_issuers():
    response = requests.get(BASE_URL_HISTORY.format("ADIN"))
    if response.status_code != 200:
        print("Failed to fetch issuer list.")
        return

    soup = BS(response.content, 'html.parser')
    options_tmp = soup.select("#Code > option")
    options_list = [option.text.strip() for option in options_tmp if not any(char.isdigit() for char in option.text)]
    # Save issuer codes to a CSV file
    pd.DataFrame(options_list, columns=["Issuer Code"]).to_csv("issuers.csv", index=False)


def fetch_issuer_details(issuer_code):
    print(f"Fetching data for issuer: {issuer_code}")
    response = requests.get(BASE_URL_DATA.format(issuer_code))

    if response.status_code != 200:
        print(f"Error loading page for {issuer_code}: {response.status_code}")
        return None

    soup = BS(response.content, 'html.parser')

    name_elements = soup.select("#izdavach > div:nth-child(1) > div.col-md-8.title")
    name = name_elements[0].get_text(strip=True) if name_elements else 'N/A'

    address_elements = soup.select("#izdavach > div:nth-child(3) > div.col-md-8")
    address = address_elements[0].get_text(strip=True) if address_elements else 'N/A'

    city_elements = soup.select("#izdavach > div:nth-child(4) > div.col-md-8")
    city = city_elements[0].get_text(strip=True) if city_elements else 'N/A'

    email_elements = soup.select("#izdavach > div:nth-child(6) > div.col-md-8")
    email = email_elements[0].get_text(strip=True) if email_elements else 'N/A'

    web_page_elements = soup.select("#izdavach > div:nth-child(7) > div.col-md-8 > a")
    web_page = web_page_elements[0]['href'] if web_page_elements else 'N/A'

    person_elements = soup.select("#izdavach > div:nth-child(8) > div.col-md-8 > span")
    person = person_elements[0].get_text(strip=True) if person_elements else 'N/A'

    phone_elements = soup.select("#izdavach > div:nth-child(9) > div.col-md-8")
    phone = phone_elements[0].get_text(strip=True) if phone_elements else 'N/A'

    company_par = soup.select("#companyProfile > p")
    company_profile = " ".join(p.get_text(strip=True) for p in company_par)

    total_prihod_2023_elements = soup.select("#red10 > td:nth-child(2)")
    total_prihod_2023 = total_prihod_2023_elements[0].get_text(strip=True) if total_prihod_2023_elements else 'N/A'

    total_po_odanocuvanje_elements = soup.select("#red11 > td:nth-child(2)")
    total_po_odanocuvanje = total_po_odanocuvanje_elements[0].get_text(strip=True) if total_po_odanocuvanje_elements else 'N/A'

    glavnina_elements = soup.select("#red12 > td:nth-child(2)")
    glavnina = glavnina_elements[0].get_text(strip=True) if glavnina_elements else 'N/A'

    vkupno_obvrski_elements = soup.select("#red13 > td:nth-child(2)")
    vkupno_obvrski = vkupno_obvrski_elements[0].get_text(strip=True) if vkupno_obvrski_elements else 'N/A'

    vkupno_sredstva_elements = soup.select("#red14 > td:nth-child(2)")
    vkupno_sredstva = vkupno_sredstva_elements[0].get_text(strip=True) if vkupno_sredstva_elements else 'N/A'

    pazar_kapital_elements = soup.select("#red15 > td:nth-child(2)")
    pazar_kapital = pazar_kapital_elements[0].get_text(strip=True) if pazar_kapital_elements else 'N/A'

    hv_isin_elements = soup.select("#symbol-data > div:nth-child(2) > div.col-md-7")
    hv_isin = hv_isin_elements[0].get_text(strip=True) if hv_isin_elements else 'N/A'

    hv_total_elements = soup.select("#symbol-data > div:nth-child(3) > div.col-md-7")
    hv_total = hv_total_elements[0].get_text(strip=True) if hv_total_elements else 'N/A'

    data = {
        "code": issuer_code,
        "name": name,
        "address": address,
        "city": city,
        "email": email,
        "web_page": web_page,
        "contact_person": person,
        "phone": phone,
        "company_profile": company_profile,
        "total_revenue_2023": total_prihod_2023,
        "profit_before_tax": total_po_odanocuvanje,
        "equity": glavnina,
        "total_liabilities": vkupno_obvrski,
        "total_assets": vkupno_sredstva,
        "market_capitalization": pazar_kapital,
        "hv_isin": hv_isin,
        "hv_total": hv_total
    }

    df_i = pd.DataFrame([data])
    return df_i



if __name__ == "__main__":
    # Get issuer list
    get_issuers()
    issuers = pd.read_csv("issuers.csv")["Issuer Code"].tolist()

    # Collect all DataFrames
    all_data = []
    with ThreadPoolExecutor(max_workers=16) as executor:
        for df in executor.map(fetch_issuer_details, issuers):
            all_data.append(df)

    # Concatenate all DataFrames into one
    final_df = pd.concat(all_data, ignore_index=True)

    # Save the final DataFrame to CSV
    final_df.to_csv("all_issuer_data.csv", index=False)
    print("Data collection complete.")
