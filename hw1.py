import pandas as pd
from selenium import webdriver
from selenium.common import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as BS
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import threading
import time

# Browser options
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Base URL for data fetching
BASE_URL = "https://www.mse.mk/mk/stats/symbolhistory/"

browser_lock = threading.Lock()

browser_pool = []

def init_browser_pool(size):
    global browser_pool
    browser_pool = [webdriver.Chrome(options=options) for _ in range(size)]

def get_browser_from_pool():
    with browser_lock:
        if browser_pool:
            return browser_pool.pop()
        else:
            return webdriver.Chrome(options=options)

def return_browser_to_pool(browser):
    with browser_lock:
        browser_pool.append(browser)

def get_issuers():
    browser = get_browser_from_pool()
    url = "https://www.mse.mk/mk/stats/symbolhistory/ADIN"
    browser.get(url)
    soup = BS(browser.page_source, 'html.parser')
    options_tmp = soup.select("#Code > option")
    options_list = [option.text.strip() for option in options_tmp if not any(char.isdigit() for char in option.text)]
    return_browser_to_pool(browser)
    return options_list

def get_last_date(issuer_code):
    try:
        df = pd.read_csv(f"{issuer_code}.csv")
        if df.empty:
            return None
        last_date = pd.to_datetime(df.tail(1)['Date']).iloc[0]
        return last_date
    except FileNotFoundError:
        return None

def fetch_data_for_issuer(issuer_code, start_date):
    browser = get_browser_from_pool()
    url = BASE_URL + issuer_code
    browser.get(url)

    now = pd.Timestamp.now()
    mnt_day_from = f"{start_date.day}.{start_date.month}."
    mnt_day_to = f"{now.day - 1}.{now.month}." if now.day > 1 else f"{(now.day - 1 + 30) % 30}.{(now.month - 1) % 12}."

    code = Select(browser.find_element(By.CSS_SELECTOR, "#Code"))
    from_date = browser.find_element(By.CSS_SELECTOR, "#FromDate")
    to_date = browser.find_element(By.CSS_SELECTOR, "#ToDate")
    btn = browser.find_element(By.CSS_SELECTOR, "#report-filter-container > ul > li.container-end > input")

    from_date.clear()
    from_date.send_keys(mnt_day_from + str(start_date.year))
    to_date.clear()
    to_date.send_keys(mnt_day_to + str(now.year))
    code.select_by_value(issuer_code)
    try:
        btn.click()
    except ElementClickInterceptedException:
        try:
            cookie_button = browser.find_element(By.CSS_SELECTOR, ".allow-button")
            cookie_button.click()
            btn.click()
        except NoSuchElementException:
            print("Cookie consent button not found.")
            raise

    soup = BS(browser.page_source, 'html.parser')
    rows = soup.select("#resultsTable > tbody > tr")
    rows = rows[::-1]

    data = []
    for row in rows:
        cells = row.select("td")
        if pd.isna(cells[1].text.strip()):
            continue
        date = cells[0].text.strip()
        month = date[3:5]
        y = date[6:]
        year_str = "20" + y[-2:]
        dic = {
            "Date": date,
            "Year": year_str,
            "Month": month,
            "Price for last transaction": cells[1].text.strip(),
            "Maximum": cells[2].text.strip(),
            "Minimum": cells[3].text.strip(),
            "Average price": cells[4].text.strip(),
            "%prom": cells[5].text.strip(),
            "Quantity": cells[6].text.strip(),
            "Traffic BEST mkd": cells[7].text.strip(),
            "Total traffic": cells[8].text.strip()
        }
        data.append(dic)

    return_browser_to_pool(browser)
    return data

def save_data(issuer_code, data):
    new_df = pd.DataFrame(data)
    try:
        existing_df = pd.read_csv(f"{issuer_code}.csv")
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    except FileNotFoundError:
        updated_df = new_df
    updated_df.to_csv(f"{issuer_code}.csv", encoding="utf-8-sig", index=False)
    print(f"Data for {issuer_code} saved/updated.")

def process_issuer_data(issuer_code):
    last_date = get_last_date(issuer_code)
    if last_date is None:
        start_date = datetime(2014, 11, 3)
    else:
        start_date = last_date + pd.Timedelta(days=1)
    data = fetch_data_for_issuer(issuer_code, start_date)
    save_data(issuer_code, data)

def get_data():
    issuers = get_issuers()
    init_browser_pool(7)
    with ThreadPoolExecutor(max_workers=7) as executor:
        executor.map(process_issuer_data, issuers)

if __name__ == '__main__':
    start_time = time.time()
    get_data()
    end_time = time.time()
    execution_time_minutes = (end_time - start_time) / 60
    print(f"Execution time: {execution_time_minutes:.2f} minutes")