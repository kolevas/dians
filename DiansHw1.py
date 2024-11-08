import os

import pandas as pd
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as BS
from concurrent.futures import ThreadPoolExecutor
import time

# Base URL for fetching data
BASE_URL = "https://www.mse.mk/mk/stats/symbolhistory/{}"


def get_issuers():
    # Retrieve all issuers listed on the Macedonian Stock Exchange website
    response = requests.get(BASE_URL.format("ADIN"))
    html_content = response.content
    soup = BS(html_content, 'html.parser')
    options_tmp = soup.select("#Code > option")
    options_list = [option.text.strip() for option in options_tmp if not any(char.isdigit() for char in option.text)]
    return options_list


def get_last_date(issuer_code):
    # Check the last date of available data
    try:
        df = pd.read_csv(f"{issuer_code}.csv")
        if df.empty:
            return None
        last_date = pd.to_datetime(df.tail(1)['Date']).iloc[0]
        return last_date
    except FileNotFoundError:
        return None


def extract_row_data(row):
    """Helper function to extract data from each row"""
    row_cells = row.select("td")
    date_str = row_cells[0].text.strip()
    year_str = date_str.split(".")[2]
    month = date_str.split(".")[1]
    return {
        "Date": date_str,
        "Year": year_str,
        "Month": month,
        "Price for last transaction": row_cells[1].text.strip(),
        "Maximum": row_cells[2].text.strip(),
        "Minimum": row_cells[3].text.strip(),
        "Average price": row_cells[4].text.strip(),
        "%prom": row_cells[5].text.strip(),
        "Quantity": row_cells[6].text.strip(),
        "Traffic BEST mkd": row_cells[7].text.strip(),
        "Total traffic": row_cells[8].text.strip()
    }


def fetch_page_data(session, url, payload):
    """Helper function to fetch data from a single page and handle pagination"""
    response = session.post(url, data=payload)
    if response.status_code != 200:
        print(f"Failed to fetch data. HTTP Status: {response.status_code}")
        return []

    soup = BS(response.content, 'html.parser')
    rows = soup.select("#resultsTable > tbody > tr")
    data = [extract_row_data(row) for row in rows]

    # Check if there's another page to paginate to
    next_button = soup.select_one(".next > a")
    if next_button:
        next_page_url = next_button.get("href")
        data.extend(fetch_page_data(session, next_page_url, payload))  # Recursive call to fetch data from next page

    return data


def fetch_data_for_year(issuer_code, year):
    """Fetch all data for a given year"""
    payload = {
        'Code': issuer_code,
        'FromDate': f"01.01.{year}",
        'ToDate': f"31.12.{year}"
    }

    print(f"Requesting data for {issuer_code} for year {year}...")

    with requests.Session() as session:
        session.headers.update({'User-Agent': 'Mozilla/5.0'})  # Set user-agent to avoid potential blocking

        # Request the data for the whole year
        data = fetch_page_data(session, BASE_URL.format(issuer_code), payload)

    # Reverse the data for the year (keeping the order as the browser would show)
    return data[::-1]


def fetch_and_save_data(issuer_code):
    try:
        last_date = get_last_date(issuer_code)
        if last_date is None:
            start_date = datetime(2014, 11, 3)  # Start from a default date if no data exists
        else:
            start_date = last_date + timedelta(days=1)  # Start from the next day after the last entry

        now = datetime.now()
        data = []

        # Fetch data for each year starting from the last available date
        for year in range(start_date.year, now.year + 1):
            year_data = fetch_data_for_year(issuer_code, year)
            if year_data:
                data.extend(year_data)

        # Save the data to CSV
        new_df = pd.DataFrame(data)
        try:
            existing_df = pd.read_csv(f"data/{issuer_code}.csv")
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        except FileNotFoundError:
            updated_df = new_df
        updated_df.to_csv(f"data/{issuer_code}.csv", encoding="utf-8-sig", index=False)
        print(f"Data for {issuer_code} saved/updated.")

    except Exception as e:
        print(f"Error fetching data for {issuer_code}: {e}")


def main():
    issuers = get_issuers()
    num_workers = 16  # Adjust number of threads based on available resources
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        executor.map(fetch_and_save_data, issuers)


if __name__ == '__main__':
    start_time = time.time()
    if not os.path.exists('data'):
        os.makedirs('data')
    main()
    end_time = time.time()
    execution_time_minutes = (end_time - start_time) / 60
    print(f"Execution time: {execution_time_minutes:.2f} minutes")
